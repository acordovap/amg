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
from spade.template import Template
from spade.message import Message

class Chord(Agent):
    async def setup(self):
        # print("<Chord> {}".format(str(self.jid).split("@")[0]))
        self.set("inversion", None)
        inversion_template = Template()
        inversion_template.set_metadata("performative", "inversion")
        self.add_behaviour(self.receiveInversion(), inversion_template)
        self.add_behaviour(self.sendChord())

    class receiveInversion(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg: # Received proposed inversion
                self.agent.set("inversion", msg.body)
            else:
                self.agent.set("inversion", None)

    class sendChord(CyclicBehaviour):
        async def run(self):
            contacts = self.presence.get_contacts()
            for i in range(CFG.no_songs):
                cntct = contacts[aioxmpp.JID.fromstr("s_" + str(i) + CFG.XMPP_SERVER)]["presence"]
                if cntct.show == PresenceShow.CHAT and cntct.status.any() == "chords":
                    self.agent.presence.set_presence(state=PresenceState(available=True, show=PresenceShow.CHAT))
                    msg = Message(to="s_" + str(i) + CFG.XMPP_SERVER)     # Instantiate the message
                    msg.set_metadata("performative", "chords")  # Set the "notes" FIPA performative
                    cl = getattr(chords, self.agent.name.split("_")[2].upper())(self.agent.name.split("_")[1].capitalize())
                    inv = self.agent.get("inversion")
                    if inv != None:
                        cl2 = getattr(chords, inv+"_inversion")(cl)
                        self.agent.set("inversion", None)
                        msg.body = ','.join(cl2)                    # Set the message content
                    else:
                        msg.body = ','.join(cl)                    # Set the message content
                    await self.send(msg)
                    await asyncio.sleep(random.randint(1, 10)/1000)
