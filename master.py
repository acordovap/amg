import config as CFG
import time
from notes import *
from songs import *
from chords import *

if __name__ == "__main__":
    receiveragent = SongAgent("receiver"+CFG.XMPP_SERVER, "receiver_password")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.

    c5 = Note_C5("note_c5"+CFG.XMPP_SERVER, ".")
    c5.start()
    d5 = Note_D5("note_d5"+CFG.XMPP_SERVER, ".")
    d5.start()
    e5 = Note_E5("note_e5"+CFG.XMPP_SERVER, ".")
    e5.start()
    f5 = Note_F5("note_f5"+CFG.XMPP_SERVER, ".")
    f5.start()
    g5 = Note_G5("note_g5"+CFG.XMPP_SERVER, ".")
    g5.start()
    a5 = Note_A5("note_a5"+CFG.XMPP_SERVER, ".")
    a5.start()
    b5 = Note_B5("note_b5"+CFG.XMPP_SERVER, ".")
    b5.start()
    #
    i = Chord_I("chord_i"+CFG.XMPP_SERVER, ".")
    i.start()
    v = Chord_V("chord_v"+CFG.XMPP_SERVER, ".")
    v.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
    print("Agents finished")
