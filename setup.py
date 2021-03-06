import time
import getpass
import config as CFG
from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour

class Setup_NotePitches(Agent):
    async def setup(self):
        print("<Setup_NotePitches> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.Behav1())

    class Behav1(OneShotBehaviour):
        async def run(self):
            self.presence.set_available()
            for i in CFG.all_notes:
                self.presence.subscribe("n_" +  i.lower() + CFG.XMPP_SERVER)

class Setup_NoteValues(Agent):
    async def setup(self):
        print("<Setup_NoteValues> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.Behav1())

    class Behav1(OneShotBehaviour):
        async def run(self):
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
            for i in range(CFG.no_songs):
                self.presence.subscribe("s_" +  str(i) + CFG.XMPP_SERVER)

class Setup_Inversions(Agent):
    async def setup(self):
        print("<Setup_Inversions> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.Behav1())

    class Behav1(OneShotBehaviour):
        async def run(self):
            self.presence.set_available()
            for i in CFG.all_notes:
                for j in CFG.all_chords:
                    jid1 = "c_" + i.lower() + "_" + j.lower() + CFG.XMPP_SERVER
                    me = self.agent.name
                    if not ("third" in me and "7" not in jid1):
                        self.presence.subscribe(jid1)

class Setup_Chords(Agent):
    async def setup(self):
        print("<Setup_Chords> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.Behav1())

    class Behav1(OneShotBehaviour):
        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)

        async def run(self):
            self.presence.on_subscribe = self.on_subscribe
            self.presence.set_available()
            for i in range(CFG.no_songs):
                self.presence.subscribe("s_" +  str(i) + CFG.XMPP_SERVER)

class Setup_Songs(Agent):
    async def setup(self):
        print("<Setup_Songs> {}".format(str(self.jid).split("@")[0]))
        self.add_behaviour(self.Behav1())

    class Behav1(OneShotBehaviour):
        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)

        async def run(self):
            self.presence.on_subscribe = self.on_subscribe
            self.presence.set_available()

if __name__ == "__main__":

    # Song
    for i in range(CFG.no_songs):
        jid1 = "s_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Setup_Songs(jid1, passwd1)
        a1.start().result()

    # Chord
    for i in CFG.all_notes:
        for j in CFG.all_chords:
            jid1 = "c_" + str(i) + "_" + str(j) + CFG.XMPP_SERVER
            passwd1 = "."
            a1 = Setup_Chords(jid1, passwd1)
            a1.start().result()

    # Inversion
    for i in CFG.inversions:
        jid1 = "i_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Setup_Inversions(jid1, passwd1)
        a1.start().result()

    # RawNote
    for i in CFG.all_notes:
        jid1 = "n_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Setup_RawNotes(jid1, passwd1)
        a1.start().result()

    #NoteValue
    for i in CFG.all_note_values:
        jid1 = "nv_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Setup_NoteValues(jid1, passwd1)
        a1.start().result()

    #NotePitch
    for i in CFG.MELODY_PITCH_RANGE:
        jid1 = "np_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Setup_NotePitches(jid1, passwd1)
        a1.start().result()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            quit_spade()
            break
