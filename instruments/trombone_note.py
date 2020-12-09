from mido import Message
import math

class TromboneMessage:
    """
    In the original Midi file, each note is represented by a number, 21 being the lowest note on 
    a keyboard and 108 being the highest. In the final file, we no longer care about the actual
    note being played, but rather the position of that note, so we will replace the 'note' value in each 
    midi message to correspond with the trombone position we desire to play. 

    Most, but not all, notes on a trombone can be assigned an integer position of 1-7. 
    However, there are contexts when a note is a 1.5 or 2.5 position. To accomodate 
    this, each position will be ten times the conventional name. 

    Ex: 
      * Position 1: note=10
      * Position 2: note=20
      * Position 3: note=30
      * Position 4: note=40
      * Position 5: note=50
      * Position 6: note=60
      * Position 7: note=70

    Many of the notes have alternate positions. Depending on the notes played before or after, we
    have preference to play the note in one position or another. For example, a fourth-line base clef
    F is typically played in first position, but if we have a second-space C just beforehand, we
    typically want to play both in sixth position.  Because of this, instead of greedily assigning positions
    to notes, we will maintain the list of potential positions until we determine we have an optimal path.
    
    """
    trombone_notes = {
        "A4": [20],
        "Ab4": [30],
        "G4": [15],
        "F#4": [25],
        "F4": [10],
        "E4": [20],
        "Eb4": [30],
        "D4": [10, 40],
        "Db4": [20, 50],
        "C4": [30, 60],
        "B3": [40, 70],
        "Bb3": [10],
        "A3": [20],
        "Ab3": [30],
        "G3": [40],
        "F#3": [50],
        "F3": [10, 60],
        "E3": [20],
        "Eb3": [30],
        "D3": [40],
        "Db3": [50],
        "C3": [60],
        "B2": [70],
        "Bb2": [10],
        "A2": [20],
        "Ab2": [30],
        "G2": [40],
        "F#2": [50],
        "F2": [60],
    }

    def __init__(self, message):
        self.original_message = message


        # Not all midi messages are notes. We only want to modify note messages
        self.is_note = hasattr(self.original_message, 'note')
        self.is_program_change = message.type == "program_change" and hasattr(message, "program")

        if not self.is_note:
            return

        self.original_note = get_note_name(self.original_message.note)
        self.potential_positions = self.trombone_notes.get(self.original_note, [])

        if len(self.potential_positions) < 1:
            raise ValueError(f"Message {self.original_message} requests note {self.original_note} which is unavailable")
        else:
            self.current_position = self.potential_positions[0]

    def to_message(self):
        if self.is_note:
            return self.original_message.copy(note=self.current_position)
        elif self.is_program_change:
            # Some midi files list the instrument as trumpet, but we want the output file to request the 58th instrument (trombone)
            return self.original_message.copy(program=58)
        else:
            return self.original_message


def get_note_name(note_number):
    notes = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    octave = math.floor(note_number / 12) - 1
    name = notes[note_number % 12]
    return f"{name}{octave}"
