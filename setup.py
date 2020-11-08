import time
import getpass
import config as CFG
from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour

class Setup_NoteValues(Agent):
    async def setup(self):
        print("<Setup_NoteValues> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.Behav1())

    class Behav1(OneShotBehaviour):
        def on_available(self, peer_jid, stanza):
            print("[{}] My friend {} is now available with show {}".format(self.agent.name, peer_jid.split("@")[0], stanza.show))

        async def run(self):
            self.presence.on_available =  self.on_available
            self.presence.set_available()
            for i in CFG.all_notes:
                self.presence.subscribe("n_" +  i.lower() + CFG.XMPP_SERVER)

class Setup_RawNotes(Agent):
    async def setup(self):
        print("<Setup_RawNotes> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.Behav1())

    class Behav1(OneShotBehaviour):
        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)

        async def run(self):
            self.presence.on_subscribe = self.on_subscribe
            self.presence.set_available()

if __name__ == "__main__":

    for i in CFG.all_notes:
        jid1 = "n_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Setup_RawNotes(jid1, passwd1)
        a1.start()

    for i in CFG.all_note_values:
        jid1 = "nv_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Setup_NoteValues(jid1, passwd1)
        a1.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            quit_spade()
            break
