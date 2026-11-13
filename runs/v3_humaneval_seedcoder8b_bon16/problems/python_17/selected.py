from typing import List

def parse_music(music_string: str) -> List[int]:
    note_map = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }
    
    # Split the input string by spaces to get individual notes
    notes = music_string.split()
    
    # Use a list comprehension to map each note to its corresponding duration
    return [note_map[note] for note in notes]

# Example usage
if __name__ == "__main__":
    print(parse_music('o o| .| o| o| .| .| .| .| o o'))