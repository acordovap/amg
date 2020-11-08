import config as CFG
import time
from spade import quit_spade
# from notes import *
from songs import *
from chords import *
from note_values import *
from note_pitches import *
from raw_notes import *

if __name__ == "__main__":

    # init songs
    for i in range(CFG.no_songs):
        jid1 = "s_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = SongAgent(jid1, passwd1)
        a1.start().result()

    # init chords
    for i in list(set(CFG.PROGRESSIONS)):
        jid1 = "c_" + CFG.SONG_KEY_SIGNATURE.lower() + "_" + str(i).lower() + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Chord(jid1, passwd1)
        a1.start()

    # init notes
    for i in CFG.all_notes: # poner solo notas de la escala
        jid1 = "n_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = RawNote(jid1, passwd1)
        a1.start().result()

    # init note all_note_values
    for i in CFG.all_note_values:
        jid1 = "nv_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = NoteValue(jid1, passwd1)
        a1.start()

    # init note all_note_pitches
    for i in CFG.MELODY_PITCH_RANGE:
        jid1 = "np_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = NotePitch(jid1, passwd1)
        a1.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            quit_spade()
            break
    print("Agents finished")
