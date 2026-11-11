import sys

def get_note_index(note):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes.index(note)

def is_transposition(melody1, melody2):
    n = len(melody1)
    shift = (get_note_index(melody2[0]) - get_note_index(melody1[0])) % 12
    
    for i in range(1, n):
        if (get_note_index(melody2[i]) - get_note_index(melody1[i])) % 12 != shift:
            return False
    return True

def is_retrograde(melody1, melody2):
    return melody1 == melody2[::-1]

def is_inversion(melody1, melody2):
    n = len(melody1)
    first_note_index = get_note_index(melody1[0])
    
    for i in range(1, n):
        interval1 = (get_note_index(melody1[i]) - first_note_index) % 12
        interval2 = (first_note_index - get_note_index(melody2[i])) % 12
        if interval1 != interval2:
            return False
    return True

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    l = int(data[0])
    melody1 = data[1:1+l]
    melody2 = data[1+l:]
    
    if is_transposition(melody1, melody2):
        print("Transposition")
    elif is_retrograde(melody1, melody2):
        print("Retrograde")
    elif is_inversion(melody1, melody2):
        print("Inversion")
    else:
        print("Nonsense")

if __name__ == "__main__":
    main()