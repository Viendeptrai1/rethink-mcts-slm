def determine_relation(l, melody1, melody2):
    # Mapping of notes to their positions in the chromatic scale
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_indices = {note: i for i, note in enumerate(notes)}

    # Convert notes to indices
    melody1_indices = [note_indices[note] for note in melody1]
    melody2_indices = [note_indices[note] for note in melody2]

    # Check for Transposition
    diff = melody2_indices[0] - melody1_indices[0]
    if all((melody2_indices[i] - melody1_indices[i]) % 12 == diff for i in range(1, l)):
        return "Transposition"

    # Check for Retrograde
    if melody2_indices[::-1] == melody1_indices:
        return "Retrograde"

    # Check for Inversion
    inverted_melody2_indices = [(notes.index(notes[melody1_indices[0]]) - (i - notes.index(notes[melody1_indices[0]])) + 12) % 12 for i in melody2_indices]
    if inverted_melody2_indices == melody1_indices:
        return "Inversion"

    return "Nonsense"

# Input reading
import sys
input = sys.stdin.read
data = input().split()
l = int(data[0])
melody1 = data[1:l+1]
melody2 = data[l+1:2*l+1]

# Determine the relation and print the result
print(determine_relation(l, melody1, melody2))