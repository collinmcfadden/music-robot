from mido import MidiTrack, MetaMessage, bpm2tempo, Message
from instruments.instrument import Instrument

class Accompaniment(Instrument):

    def __init__(self, track, tempo_bpm, offset_ticks):
        super().__init__(track, tempo_bpm)
        self.offset_ticks = offset_ticks

    def create_track(self):
        track = MidiTrack()
        offset_added = False
        
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.tempo_bpm), time=0))
        for msg in self.original_track:
            if not offset_added and hasattr(msg, 'note'):
                track.append(Message('note_on', note=100, velocity=1, time=self.offset_ticks))
                track.append(Message('note_off', note=100, velocity=1, time=0))
                offset_added = True
            track.append(msg)

        return track
