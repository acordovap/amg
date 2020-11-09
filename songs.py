import config as CFG
import asyncio
import aioxmpp
from spade import quit_spade
from aioxmpp import PresenceState, PresenceShow
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import FSMBehaviour, State
from spade.template import Template
import mingus.core.chords as chords
from mingus.containers.note import Note
from mingus.containers import NoteContainer
from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers import Composition
from mingus.midi import fluidsynth
from mingus.extra import lilypond
from mingus.midi import midi_file_out

S_RECEIVE_CHORD = "S_RECEIVE_CHORD"
S_RECEIVE_NOTE  = "S_RECEIVE_NOTE"
S_PUBLISH_SONG  = "S_PUBLISH_SONG"
S_FINISHED      = "S_FINISHED"

class SongAgent(Agent):
    async def setup(self):
        # print("<SongAgent> {}".format(str(self.jid).split("@")[0]))
        fsm = SongBehaviour()
        fsm.add_state(name=S_RECEIVE_CHORD, state=SReceiveChordState(), initial=True)
        fsm.add_state(name=S_RECEIVE_NOTE, state=SReceiveNoteState())
        fsm.add_state(name=S_PUBLISH_SONG, state=SPublishSongState())
        fsm.add_state(name=S_FINISHED, state=SFinishedState())
        fsm.add_transition(source=S_RECEIVE_CHORD, dest=S_RECEIVE_CHORD)
        fsm.add_transition(source=S_RECEIVE_CHORD, dest=S_RECEIVE_NOTE)
        fsm.add_transition(source=S_RECEIVE_CHORD, dest=S_PUBLISH_SONG)
        fsm.add_transition(source=S_RECEIVE_NOTE, dest=S_RECEIVE_NOTE)
        fsm.add_transition(source=S_RECEIVE_NOTE, dest=S_RECEIVE_CHORD)
        fsm.add_transition(source=S_PUBLISH_SONG, dest=S_FINISHED)
        fsm.add_transition(source=S_FINISHED, dest=S_FINISHED)
        chords_template = Template()
        notes_template = Template()
        chords_template.set_metadata("performative", "chords")
        notes_template.set_metadata("performative", "notes")
        self.set("chords_template", chords_template)
        self.set("notes_template", notes_template)
        self.add_behaviour(fsm, chords_template|notes_template)

class SongBehaviour(FSMBehaviour):
    async def on_start(self):
        self.agent.set("current_bar_no", 0) # inicializa "current_bar_no" en 0
        # self.agent.set("tempo", 120)
        # self.agent.set("key", "C")
        self.agent.set("melody_track", Track())
        self.agent.set("accompaniment_track", Track())
        self.agent.set("current_melody_bar", Bar(CFG.SONG_KEY_SIGNATURE, CFG.SONG_TIME_SIGNATURE))
        self.agent.set("current_accompaniment_bar", Bar(CFG.SONG_KEY_SIGNATURE, CFG.SONG_TIME_SIGNATURE))

class SReceiveChordState(State):
    async def on_start(self):
        self.agent.presence.set_presence(state=PresenceState(available=True, show=PresenceShow.CHAT))
        self.agent.presence.set_presence(status="chords")

    async def run(self):
        cbn = self.agent.get("current_bar_no")
        if cbn < CFG.SONG_LENGTH: # falta sacar con modulo, de momento es un acorde por barra
            msg = await self.receive()
            if msg:
                if self.agent.get("chords_template").match(msg):
                    if chords.determine_triad(getattr(chords, CFG.PROGRESSIONS[cbn])(CFG.SONG_KEY_SIGNATURE), True) == chords.determine_triad(msg.body.split(','), True):
                        cab = self.agent.get("current_accompaniment_bar")
                        cab.place_notes(msg.body.split(','), 1) # de momento es un acorde por barra
                        at = self.agent.get("accompaniment_track")
                        at.add_bar(cab)
                        self.agent.set("current_accompaniment_bar", Bar(CFG.SONG_KEY_SIGNATURE, CFG.SONG_TIME_SIGNATURE))
                        self.agent.set("accompaniment_track", at)
                        self.set_next_state(S_RECEIVE_NOTE)
                    else:
                        self.set_next_state(S_RECEIVE_CHORD) # Continúa en el mismo estado
                else:
                    self.set_next_state(S_RECEIVE_CHORD) # Continúa en el mismo estado
            else:
                self.set_next_state(S_RECEIVE_CHORD) # Continúa en el mismo estado
        else:
            self.set_next_state(S_PUBLISH_SONG)

class SReceiveNoteState(State):
    async def on_start(self):
        self.agent.presence.set_presence(state=PresenceState(available=True, show=PresenceShow.CHAT))
        self.agent.presence.set_presence(status="notes")

    async def run(self):
        cbn = self.agent.get("current_bar_no")
        msg = await self.receive()
        if msg:
            if self.agent.get("notes_template").match(msg):
                if Note(msg.body.split(",")[0]).name in getattr(chords, CFG.PROGRESSIONS[cbn])(CFG.SONG_KEY_SIGNATURE):
                    cmb = self.agent.get("current_melody_bar")
                    if cmb.current_beat + 1/float(msg.body.split(",")[1]) <= cmb.length:
                        cmb.place_notes(msg.body.split(",")[0], int(msg.body.split(",")[1])) # de momento 4 notas por barra
                        if cmb.current_beat == cmb.length: # chechar si llena, entonces agregar a melody_track
                            mt = self.agent.get("melody_track")
                            mt.add_bar(cmb)
                            self.agent.set("melody_track", mt)
                            self.agent.set("current_melody_bar", Bar(CFG.SONG_KEY_SIGNATURE, CFG.SONG_TIME_SIGNATURE))
                            self.agent.set("current_bar_no", cbn+1)
                            print("{}: {}/{}".format(self.agent.name, cbn+1, CFG.SONG_LENGTH)) # falta sacar con modulo, de momento es un acorde por barra
                            self.set_next_state(S_RECEIVE_CHORD)
                        else:
                            self.agent.set("current_melody_bar", cmb)
                            self.set_next_state(S_RECEIVE_NOTE)
                    else:
                        self.set_next_state(S_RECEIVE_NOTE) # Continúa en el mismo estado
                else:
                    self.set_next_state(S_RECEIVE_NOTE) # Continúa en el mismo estado
            else:
                self.set_next_state(S_RECEIVE_NOTE) # Continúa en el mismo estado
        else:
            self.set_next_state(S_RECEIVE_NOTE) # Continúa en el mismo estado


class SPublishSongState(State):
    async def on_start(self):
        self.agent.presence.set_presence(state=PresenceState(available=True, show=PresenceShow.DND))
        self.agent.presence.set_presence(status="")

    async def run(self):
        while await self.receive(): # flush messages
            pass

        c = Composition()
        c.set_author("amg")
        c.set_title(CFG.OUTPUT_PREFIX + self.agent.name)
        c.add_track(self.agent.get("melody_track"))
        c.add_track(self.agent.get("accompaniment_track"))
        # fluidsynth.init("4U-Yamaha C5 Grand-v1.5.sf2", "alsa")
        # fluidsynth.play_Composition(c)
        midi_file_out.write_Composition(CFG.OUTPUT_FOLDER+CFG.OUTPUT_PREFIX+self.agent.name+".mid", c, CFG.SONG_TEMPO)
        l = lilypond.from_Composition(c)
        # print(l)
        lilypond.to_pdf(l, CFG.OUTPUT_FOLDER+CFG.OUTPUT_PREFIX+self.agent.name)
        self.agent.presence.set_presence(state=PresenceState(available=True, show=PresenceShow.AWAY))
        self.set_next_state(S_FINISHED)

class SFinishedState(State):
    async def on_start(self):
        self.agent.presence.set_presence(state=PresenceState(available=True, show=PresenceShow.AWAY))

    async def run(self):
        while await self.receive(): # flush messages
            pass
        self.set_next_state(S_FINISHED)
