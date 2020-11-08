import config as CFG
import asyncio
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

class SongAgent(Agent):
    async def setup(self):
        fsm = SongBehaviour()
        fsm.add_state(name=S_RECEIVE_CHORD, state=SReceiveChordState(), initial=True)
        fsm.add_state(name=S_RECEIVE_NOTE, state=SReceiveNoteState())
        fsm.add_state(name=S_PUBLISH_SONG, state=SPublishSongState())
        fsm.add_transition(source=S_RECEIVE_CHORD, dest=S_RECEIVE_CHORD)
        fsm.add_transition(source=S_RECEIVE_CHORD, dest=S_RECEIVE_NOTE)
        fsm.add_transition(source=S_RECEIVE_CHORD, dest=S_PUBLISH_SONG)
        fsm.add_transition(source=S_RECEIVE_NOTE, dest=S_RECEIVE_NOTE)
        fsm.add_transition(source=S_RECEIVE_NOTE, dest=S_RECEIVE_CHORD)
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
            self.set_next_state(S_PUBLISH_SONG)
class SReceiveNoteState(State):
    async def run(self):
        cbn = self.agent.get("current_bar_no")
        msg = await self.receive()
        if msg:
            if self.agent.get("notes_template").match(msg):
                if Note(msg.body).name in getattr(chords, CFG.PROGRESSIONS[cbn])(CFG.SONG_KEY_SIGNATURE):
                    cmb = self.agent.get("current_melody_bar")
                    # checar si va a caber con el tamaño, puede ser en el if de arriba?
                    cmb.place_notes(msg.body, 4) # de momento 4 notas por barra
                    if cmb.current_beat == cmb.length: # chechar si llena, entonces agregar a melody_track
                        mt = self.agent.get("melody_track")
                        mt.add_bar(cmb)
                        self.agent.set("melody_track", mt)
                        self.agent.set("current_melody_bar", Bar(CFG.SONG_KEY_SIGNATURE, CFG.SONG_TIME_SIGNATURE))
                        self.agent.set("current_bar_no", cbn+1)
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


class SPublishSongState(State):
    async def run(self):
        c = Composition()
        c.set_author('amg')
        c.set_title('Composition')
        c.add_track(self.agent.get("melody_track"))
        c.add_track(self.agent.get("accompaniment_track"))
        # fluidsynth.init("4U-Yamaha C5 Grand-v1.5.sf2", "alsa")
        # fluidsynth.play_Composition(c)
        midi_file_out.write_Composition("amg_composition.mid", c, CFG.SONG_TEMPO)
        l = lilypond.from_Composition(c)
        # print(l)
        lilypond.to_pdf(l, "amg_composition")
