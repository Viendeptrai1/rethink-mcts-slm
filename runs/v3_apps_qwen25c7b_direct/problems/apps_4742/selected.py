def find_relation(l, melody1, melody2):
    # Define the twelve notes
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Function to get the index of a note
    def get_index(note):
        return notes.index(note)
    
    # Function to perform transposition
    def transpose(melody, n):
        return [notes[(get_index(note) + n) % 12] for note in melody]
    
    # Function to check if two melodies are the same
    def is_same(melody1, melody2):
        return melody1 == melody2
    
    # Check for transposition
    for i in range(12):
        if is_same(transpose(melody1, i), melody2):
            return "Transposition"
    
    # Check for retrograde
    if is_same(melody1[::-1], melody2):
        return "Retrograde"
    
    # Check for inversion
    if is_same([notes[(get_index(note) - get_index(melody1[0])) % 12] for note in melody1[1:]], melody2[1:]):
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