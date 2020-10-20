import config as CFG
import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class Chord_I(Agent):
    class sendChord(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "chords")  # Set the "chords" FIPA performative
            #msg.body = "[\"C\", \"E\", \"G\"]"                    # Set the message content
            msg.body = "C,E,G"
            await self.send(msg)
            await asyncio.sleep(1)

    async def setup(self):
        b = self.sendChord()
        self.add_behaviour(b)

class Chord_V(Agent):
    class sendChord(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "chords")  # Set the "chords" FIPA performative
            #msg.body = "[\"G\", \"B\", \"D\"]"                    # Set the message content
            msg.body = "G,B,D"
            await self.send(msg)
            await asyncio.sleep(1)

    async def setup(self):
        b = self.sendChord()
        self.add_behaviour(b)
