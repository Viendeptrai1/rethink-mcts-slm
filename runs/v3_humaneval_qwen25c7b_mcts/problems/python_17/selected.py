from typing import List

def parse_music(music_string: str) -> List[int]:
    """ Parse the input string and return a list of integers representing the number of beats for each note. """
    notes = music_string.split()
    durations = []
    for note in notes:
        if note == 'o':
            durations.append(4)
        elif note == 'o|':
            durations.append(2)
        elif note == '.|':
            durations.append(1)
    return durations