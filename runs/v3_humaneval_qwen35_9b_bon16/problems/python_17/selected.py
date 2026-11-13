from typing import List


def parse_music(music_string: str) -> List[int]:
    beats_map = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }
    
    result = []
    i = 0
    n = len(music_string)
    
    while i < n:
        if i + 1 < n and music_string[i] == 'o' and music_string[i+1] == '|':
            result.append(2)
            i += 2
        elif music_string[i] == '.':
            result.append(1)
            i += 2
        elif music_string[i] == 'o':
            result.append(4)
            i += 1
        else:
            i += 1
            
    return result