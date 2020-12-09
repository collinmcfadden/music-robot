
class Instrument:

    def __init__(self, track, tempo_bpm):
        self.original_track = track
        self.tempo_bpm = tempo_bpm

    def create_track(self):
        return self.original_track

