import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        l = int(next(iterator))
        melody1 = []
        for _ in range(l):
            melody1.append(next(iterator))
        melody2 = []
        for _ in range(l):
            melody2.append(next(iterator))
    except StopIteration:
        print("Nonsense")
        return

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_to_idx = {note: i for i, note in enumerate(notes)}

    def to_int(melody):
        return [note_to_idx[n] for n in melody]

    ints1 = to_int(melody1)
    ints2 = to_int(melody2)

    # Check Transposition
    is_transposition = True
    diff = ints2[0] - ints1[0]
    for i in range(l):
        if (ints2[i] - ints1[i]) != diff:
            is_transposition = False
            break
    
    if is_transposition:
        print("Transposition")
        return

    # Check Retrograde
    is_retrograde = True
    for i in range(l):
        if ints2[i] != ints1[l - 1 - i]:
            is_retrograde = False
            break
    
    if is_retrograde:
        print("Retrograde")
        return

    # Check Inversion
    is_inversion = True
    first_note = ints1[0]
    for i in range(l):
        # The interval from first note in original is (ints1[i] - first_note)
        # In inversion, this interval is negated: new_val = first_note - (ints1[i] - first_note)
        # Which simplifies to: new_val = 2 * first_note - ints1[i]
        expected = 2 * first_note - ints1[i]
        # Wrap around modulo 12
        expected = expected % 12
        if ints2[i] != expected:
            is_inversion = False
            break
    
    if is_inversion:
        print("Inversion")
        return

    print("Nonsense")

if __name__ == "__main__":
    solve()