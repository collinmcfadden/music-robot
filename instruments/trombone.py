from instruments.trombone_note import TromboneMessage
from mido import MidiTrack, MetaMessage, bpm2tempo
from instruments.instrument import Instrument


class Trombone(Instrument):

    def __init__(self, track, tempo_bpm):
        super().__init__(track, tempo_bpm)

    def create_track(self):
        messages = []

        for msg in self.original_track:
            messages.append(TromboneMessage(msg))
        
        # Run fancy algo to get optimal slide positions
        # For now, greedily select the smallest slide position
        track = MidiTrack()
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.tempo_bpm), time=0))
        for msg in messages:
            track.append(msg.to_message())

        return track

    def get_channel_numnber(self):
        for msg in self.original_track:
            if hasattr(msg, "channel"):
                return msg.channel


def is_trombone_track(track):
    """
    In Midi files, a 'program_change' message indicates which musical instrument the midi player should use 
    to play the track. On a standard midi player, brass instruments are represented by the numbers ranging
    from 57-64.
        Ex. program_change channel=1 program=58 time=0
        Indicates track 1 should be played with instrument 58 (trombome) on the midi output device.
    """
    for message in track:
        if message.type == "program_change" and hasattr(message, "program"):  
            return 56 < message.program and message.program < 65
    return False

    
        