import config as CFG
import time
import asyncio
import random
from aioxmpp import PresenceState, PresenceShow
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.template import Template
from spade.message import Message

class RawNote(Agent):
    class receiveNoteValue(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                print("msg: " + msg.body)

    async def setup(self):
        print("<RawNote> {}".format(str(self.jid).split("@")[0]))
        notevalues_template = Template()
        notevalues_template.set_metadata("performative", "notevalues")
        self.add_behaviour(self.receiveNoteValue(), notevalues_template)
        # self.presence.set_presence(state=PresenceState( state=PresenceState(True, PresenceShow.CHAT)))
