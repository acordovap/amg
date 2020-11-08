import config as CFG
import time
import asyncio
import random
import aioxmpp
from aioxmpp import PresenceState, PresenceShow
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class NotePitch(Agent):
    async def setup(self):
        # print("<NotePitch> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.sendNotePitch())

    class sendNotePitch(CyclicBehaviour):
        async def run(self):
            contacts = self.presence.get_contacts()
            for i in CFG.all_notes:
                if contacts[aioxmpp.JID.fromstr("n_" + i.lower() + CFG.XMPP_SERVER)]["presence"].show == PresenceShow.NONE:
                    msg = Message(to="n_" + i.lower() + CFG.XMPP_SERVER)     # Instantiate the message
                    msg.set_metadata("performative", "notepitch")  # Set the "notes" FIPA performative
                    msg.body = self.agent.name.split("_")[1]                    # Set the message content
                    await self.send(msg)
                    await asyncio.sleep(random.randint(1, 10)/1000)
