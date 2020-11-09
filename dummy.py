import config as CFG
import time
from aioxmpp import PresenceState, PresenceShow
from spade import quit_spade
from songs import *
from chords import *
from inversions import *
from note_values import *
from note_pitches import *
from raw_notes import *

if __name__ == "__main__":

    # init songs
    s = []
    for i in range(CFG.no_songs):
        jid1 = "s_" + str(i) + CFG.XMPP_SERVER
        passwd1 = "."
        s.append(SongAgent(jid1, passwd1) )
        s[i].start().result()

    # init chords
    for i in list(set(CFG.PROGRESSIONS)):
        jid1 = "c_" + CFG.SONG_KEY_SIGNATURE.lower() + "_" + str(i).lower() + CFG.XMPP_SERVER
        passwd1 = "."
        a1 = Chord(jid1, passwd1)
        a1.start().result()

    # init inversions
    # for i in CFG.inversions:
    #     jid1 = "i_" + str(i) + CFG.XMPP_SERVER
    #     passwd1 = "."
    #     a1 = Inversion(jid1, passwd1)
    #     a1.start()

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

    keepgoing = True
    while keepgoing:
        try:
            keepgoing = not all(i.presence.state.show == PresenceShow.AWAY for i in s)
            time.sleep(1)
            # for i in s:
            #     if i.presence.state.show != PresenceShow.AWAY:

        except KeyboardInterrupt:
            quit_spade()
            break
    print("Agents finished")
