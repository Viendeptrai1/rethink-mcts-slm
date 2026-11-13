def find_relation(l, melody1, melody2):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def transposition_check(melody1, melody2):
        shift = (notes.index(melody2[0]) - notes.index(melody1[0])) % 12
        return all((notes.index(melody2[i]) - notes.index(melody1[i])) % 12 == shift for i in range(l))
    
    def retrograde_check(melody1, melody2):
        return melody1 == melody2[::-1]
    
    def inversion_check(melody1, melody2):
        if melody2[0] != melody1[0]:
            return False
        first_note = notes.index(melody1[0])
        return all((notes.index(melody1[0]) - notes.index(melody2[i])) % 12 == (notes.index(melody1[i]) - first_note) % 12 for i in range(1, l))
    
    if transposition_check(melody1, melody2):
        return "Transposition"
    if retrograde_check(melody1, melody2):
        return "Retrograde"
    if inversion_check(melody1, melody2):
        return "Inversion"
    return "Nonsense"

import sys

input = sys.stdin.read
data = input().split()

l = int(data[0])
melody1 = data[1:l+1]
melody2 = data[l+1:2*l+1]

print(find_relation(l, melody1, melody2))