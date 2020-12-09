from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo 
import math

from instruments.trombone import Trombone, is_trombone_track
from instruments.accompaniment import Accompaniment
from output_ports.trombone_port import PrintPort
from output_ports.port_splitter import PortSplitter


mid = MidiFile('original_midi\\tchaikovsky_sugar_plum.mid')
BPM = 100
ticksperbeat = mid.ticks_per_beat
for num, track in enumerate(mid.tracks):
    for message in track:
        if message.type == "set_tempo":
            print(message)

accompaniment_offset = math.floor(ticksperbeat / 4)

# Create midi file
new_midi = MidiFile(type=1)
# new_midi.ticks_per_beat = mid.ticks_per_beat
trombone_channel_number = None

# Determine instrument for tracks and create their new tracks with any necessary message updates
for num, track in enumerate(mid.tracks):
    # If multiple Midi channels are listed as brass/trombone channels, convert the first
    # to be our trombone part and conserve the other ones as accompaniments
    if is_trombone_track(track) and trombone_channel_number is None:
        trombone = Trombone(track, BPM)
        new_midi.tracks.append(trombone.create_track())
        trombone_channel_number = trombone.get_channel_numnber()
    else:
        new_midi.tracks.append(Accompaniment(track, BPM, accompaniment_offset).create_track())

output_port = PortSplitter(trombone_channel_number)

for msg in new_midi.play():
    output_port.send(msg)



