def find_relation(l, melody1, melody2):
    # Define the twelve notes
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Function to calculate the index of a note
    def get_index(note):
        return notes.index(note)
    
    # Function to perform transposition
    def transpose(melody, n):
        return [notes[(get_index(note) + n) % 12] for note in melody]
    
    # Function to perform inversion
    def invert(melody):
        first_note = melody[0]
        return [first_note] + [notes[(get_index(first_note) - get_index(note)) % 12] for note in melody[1:]]
    
    # Check for transposition
    diff = [get_index(melody2[i]) - get_index(melody1[i]) for i in range(l)]
    if len(set(diff)) == 1 and all(d % 12 == diff[0] for d in diff):
        return "Transposition"
    
    # Check for retrograde
    if melody2 == melody1[::-1]:
        return "Retrograde"
    
    # Check for inversion
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