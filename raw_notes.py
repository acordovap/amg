import config as CFG
import time
import asyncio
import random
import aioxmpp
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
            if msg: # Received proposed duration
                fn = self.agent.get("full_note")
                fn[2] = msg.body
                self.agent.set("full_note", fn)

    class receiveNotePitch(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg: # Received proposed pitch
                fn = self.agent.get("full_note")
                fn[1] = msg.body
                self.agent.set("full_note", fn)

    class sendFullNote(CyclicBehaviour):
        async def run(self):
            contacts = self.presence.get_contacts()
            for i in range(CFG.no_songs):
                cntct = contacts[aioxmpp.JID.fromstr("s_" + str(i) + CFG.XMPP_SERVER)]["presence"]
                if cntct.show == PresenceShow.CHAT and cntct.status.any() == "notes":
                #if contacts[aioxmpp.JID.fromstr("s_" + str(i) + CFG.XMPP_SERVER)]["presence"].show == PresenceShow.NONE:
                    fn = self.agent.get("full_note")
                    if fn[1] != None and fn[2] != None:
                        msg = Message(to="s_" + str(i) + CFG.XMPP_SERVER)   # Instantiate the message
                        msg.set_metadata("performative", "notes")   # Set the "notes" FIPA performative
                        msg.body = fn[0]+"-"+str(fn[1])+","+str(fn[2])   # Set the message content
                        await self.send(msg)
                        # se podría implementar un fllush de la nota, se tendría que o salir del for o enviar a todas las songs
                        await asyncio.sleep(random.randint(1, 10)/1000)

    async def setup(self):
        # print("<RawNote> {}".format(str(self.jid).split("@")[0]))
        self.set("full_note", [self.name.split("_")[1].capitalize(), None, None])
        notevalues_template = Template()
        notepitch_template = Template()
        notes_template = Template()
        notevalues_template.set_metadata("performative", "notevalues")
        notepitch_template.set_metadata("performative", "notepitch")
        notes_template.set_metadata("performative", "notes")
        self.add_behaviour(self.receiveNoteValue(), notevalues_template)
        self.add_behaviour(self.receiveNotePitch(), notepitch_template)
        self.add_behaviour(self.sendFullNote(), notes_template)

        # self.presence.set_presence(state=PresenceState( state=PresenceState(True, PresenceShow.CHAT)))
