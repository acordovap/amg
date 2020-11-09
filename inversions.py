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

class Inversion(Agent):
    async def setup(self):
        # print("<Inversion> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.sendInversion())

    class sendInversion(CyclicBehaviour):
        async def run(self):
            contacts = self.presence.get_contacts()
            for i in list(set(CFG.PROGRESSIONS)):
                jid1 = "c_" + CFG.SONG_KEY_SIGNATURE.lower() + "_" + i.lower() + CFG.XMPP_SERVER
                me = self.agent.name
                if not ("third" in me and "7" not in jid1):
                    if contacts[aioxmpp.JID.fromstr(jid1)]["presence"].show == PresenceShow.CHAT:
                        msg = Message(to=jid1)     # Instantiate the message
                        msg.set_metadata("performative", "inversion")  # Set the "inversion" FIPA performative
                        msg.body = self.agent.name.split("_")[1]
                        await self.send(msg)
                        await asyncio.sleep(random.randint(1, 10)/1000)
