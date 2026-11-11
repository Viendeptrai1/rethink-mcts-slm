def find_relation(l, melody1, melody2):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    # Check for Retrograde
    if melody1 == melody2[::-1]:
        return "Retrograde"
    
    # Check for Transposition
    def transpose(melody, shift):
        return [notes[(notes.index(note) + shift) % 12] for note in melody]
    
    for i in range(12):
        if melody2 == transpose(melody1, i):
            return "Transposition"
    
    # Check for Inversion
    def invert(melody):
        first_note = melody[0]
        inverted_melody = [first_note]
        for note in melody[1:]:
            interval = (notes.index(note) - notes.index(first_note)) % 12
            inverted_note = notes[(notes.index(first_note) - interval) % 12]
            inverted_melody.append(inverted_note)
        return inverted_melody
    
    if melody2 == invert(melody1):
        return "Inversion"
    
    return "Nonsense"

# Read input
import sys
input = sys.stdin.read
data = input().split()

l = int(data[0])
melody1 = data[1:l+1]
melody2 = data[l+1:2*l+1]

# Find and print the relation
print(find_relation(l, melody1, melody2))