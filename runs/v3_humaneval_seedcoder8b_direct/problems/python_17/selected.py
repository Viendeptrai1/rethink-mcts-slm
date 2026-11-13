from typing import List

def parse_music(music_string: str) -> List[int]:
    note_durations = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }
    
    # Split the input string by spaces to get individual notes
    notes = music_string.split()
    
    # Map each note to its corresponding duration
    durations = [note_durations[note] for note in notes]
    
    return durations