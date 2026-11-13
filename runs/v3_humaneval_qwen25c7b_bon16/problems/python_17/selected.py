from typing import List

def parse_music(music_string: str) -> List[int]:
    note_legend = {'o': 4, 'o|': 2, '.|': 1}
    return [note_legend[note] for note in music_string.split()]