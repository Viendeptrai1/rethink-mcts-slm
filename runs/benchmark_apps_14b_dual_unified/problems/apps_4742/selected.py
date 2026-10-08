def note_to_index(note):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes.index(note)

def index_to_note(index):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[index % 12]

def is_transposition(melody1, melody2):
    diff = (note_to_index(melody2[0]) - note_to_index(melody1[0])) % 12
    for i in range(1, len(melody1)):
        if (note_to_index(melody2[i]) - note_to_index(melody1[i])) % 12 != diff:
            return False
    return True

def is_retrograde(melody1, melody2):
    return melody1 == melody2[::-1]

def is_inversion(melody1, melody2):
    if melody1[0] != melody2[0]:
        return False
    first_note_index = note_to_index(melody1[0])
    for i in range(1, len(melody1)):
        if (note_to_index(melody2[i]) - first_note_index) % 12 != (first_note_index - note_to_index(melody1[i])) % 12:
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