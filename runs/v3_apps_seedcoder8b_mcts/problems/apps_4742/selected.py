def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    l = int(data[0])
    melody1 = data[1:l+1]
    melody2 = data[l+1:2*l+1]
    
    note_to_semitone = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
        'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
    }
    
    semitone_to_note = {v: k for k, v in note_to_semitone.items()}
    
    def is_transposition(melody1, melody2):
        if len(melody1) != len(melody2):
            return False
        shift = (note_to_semitone[melody2[0]] - note_to_semitone[melody1[0]]) % 12
        return all((note_to_semitone[melody2[i]] - note_to_semitone[melody1[i]]) % 12 == shift for i in range(len(melody1)))
    
    def is_retrograde(melody1, melody2):
        return melody1 == melody2[::-1]
    
    def is_inversion(melody1, melody2):
        if len(melody1) != len(melody2):
            return False
        first_note = melody1[0]
        inverted_melody = [first_note] + [semitone_to_note[(note_to_semitone[first_note] - note_to_semitone[note]) % 12] for note in melody1[1:]]
        return inverted_melody == melody2
    
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