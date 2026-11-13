from typing import List


def parse_music(music_string: str) -> List[int]:
    beat_map = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }
    tokens = music_string.split()
    return [beat_map[token] for token in tokens]