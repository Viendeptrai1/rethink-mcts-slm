def dodecaphony_relation():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    l = int(data[0])
    melody1 = data[1:l+1]
    melody2 = data[l+1:2*l+1]
    
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_to_index = {note: i for i, note in enumerate(notes)}
    
    def transpose(melody, n):
        return [notes[(note_to_index[note] + n) % 12] for note in melody]
    
    def is_transposition(melody1, melody2):
        for i in range(12):
            if transpose(melody1, i) == melody2:
                return True
        return False
    
    def is_retrograde(melody1, melody2):
        return melody1 == melody2[::-1]
    
    def is_inversion(melody1, melody2):
        if melody1[0] != melody2[0]:
            return False
        first_note_index = note_to_index[melody1[0]]
        inverted_melody = [melody1[0]] + [
            notes[(first_note_index - note_to_index[note]) % 12] for note in melody1[1:]
        ]
        return inverted_melody == melody2
    
    if is_transposition(melody1, melody2):
        print("Transposition")
    elif is_retrograde(melody1, melody2):
        print("Retrograde")
    elif is_inversion(melody1, melody2):
        print("Inversion")
    else:
        print("Nonsense")