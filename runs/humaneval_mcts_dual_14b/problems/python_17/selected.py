from typing import List

def parse_music(music_string: str) -> List[int]:
    # Define a dictionary to map note symbols to their beat values
    note_to_beats = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }
    
    # Split the input string into individual note symbols
    notes = music_string.split()
    
    # Convert each note symbol to its corresponding beat value
    beats = [note_to_beats[note] for note in notes]
    
    return beats