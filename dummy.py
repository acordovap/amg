import config as CFG
import time
from spade import quit_spade
from notes import *
from songs import *
from chords import *
from note_values import *
from raw_notes import *

if __name__ == "__main__":

    # init notes
    for i in CFG.all_notes:
        jid1 = "n_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = RawNote(jid1, passwd1)
        a1.start()

    # init note all_note_values
    for i in CFG.all_note_values:
        jid1 = "nv_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = NoteValue(jid1, passwd1)
        a1.start()



    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            quit_spade()
            break
    print("Agents finished")
