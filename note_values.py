import config as CFG
import time
import asyncio
import random
from aioxmpp import PresenceState, PresenceShow
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class NoteValue(Agent):
    async def setup(self):
        self.add_behaviour(self.sendNoteValue())

    class sendNoteValue(OneShotBehaviour):
        def on_available(self, peer_jid, stanza):
            if stanza.show == PresenceShow.CHAT:
                msg = Message(to=peer_jid.split("@")[0]+CFG.XMPP_SERVER)     # Instantiate the message
                msg.set_metadata("performative", "notevalues")  # Set the "notes" FIPA performative
                msg.body = self.agent.name.split("_")[1]                    # Set the message content
                await self.send(msg)

        async def run(self):
            self.presence.on_available =  self.on_available
            #self.presence.set_available()
