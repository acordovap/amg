import config as CFG
import time
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class Note_C5(Agent):
    class sendNote(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "notes")  # Set the "notes" FIPA performative
            msg.body = "C-5"                    # Set the message content
            await self.send(msg)
            await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        b = self.sendNote()
        self.add_behaviour(b)

class Note_D5(Agent):
    class sendNote(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "notes")  # Set the "notes" FIPA performative
            msg.body = "D-5"                    # Set the message content
            await self.send(msg)
            await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        b = self.sendNote()
        self.add_behaviour(b)

class Note_E5(Agent):
    class sendNote(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "notes")  # Set the "notes" FIPA performative
            msg.body = "E-5"                    # Set the message content
            await self.send(msg)
            await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        b = self.sendNote()
        self.add_behaviour(b)

class Note_F5(Agent):
    class sendNote(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "notes")  # Set the "notes" FIPA performative
            msg.body = "F-5"                    # Set the message content
            await self.send(msg)
            await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        b = self.sendNote()
        self.add_behaviour(b)

class Note_G5(Agent):
    class sendNote(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "notes")  # Set the "notes" FIPA performative
            msg.body = "G-5"                    # Set the message content
            await self.send(msg)
            await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        b = self.sendNote()
        self.add_behaviour(b)

class Note_A5(Agent):
    class sendNote(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "notes")  # Set the "notes" FIPA performative
            msg.body = "A-5"                    # Set the message content
            await self.send(msg)
            await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        b = self.sendNote()
        self.add_behaviour(b)

class Note_B5(Agent):
    class sendNote(CyclicBehaviour):
        async def run(self):
            msg = Message(to="receiver"+CFG.XMPP_SERVER)     # Instantiate the message
            msg.set_metadata("performative", "notes")  # Set the "notes" FIPA performative
            msg.body = "B-5"                    # Set the message content
            await self.send(msg)
            await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        b = self.sendNote()
        self.add_behaviour(b)
