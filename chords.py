import config as CFG
import time
import asyncio
import random
import aioxmpp
from aioxmpp import PresenceState, PresenceShow
from spade.agent import Agent
import mingus.core.chords as chords
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class Chord(Agent):
    async def setup(self):
        # print("<Chord> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.sendChord())

    class sendChord(CyclicBehaviour):
        async def run(self):
            contacts = self.presence.get_contacts()
            for i in range(CFG.no_songs):
                cntct = contacts[aioxmpp.JID.fromstr("s_" + str(i) + CFG.XMPP_SERVER)]["presence"]
                if cntct.show == PresenceShow.CHAT and cntct.status.any() == "chords":
                    msg = Message(to="s_" + str(i) + CFG.XMPP_SERVER)     # Instantiate the message
                    msg.set_metadata("performative", "chords")  # Set the "notes" FIPA performative
                    cl = getattr(chords, self.agent.name.split("_")[2].upper())(self.agent.name.split("_")[1].capitalize())
                    msg.body = ','.join(cl)                    # Set the message content
                    await self.send(msg)
                    await asyncio.sleep(random.randint(1, 10)/1000)
