import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return

    if not input_data:
        return

    iterator = iter(input_data)
    try:
        l = int(next(iterator))
        melody1 = [next(iterator) for _ in range(l)]
        melody2 = [next(iterator) for _ in range(l)]
    except StopIteration:
        return

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_to_int = {note: i for i, note in enumerate(notes)}

    def get_ints(melody):
        return [note_to_int[n] for n in melody]

    ints1 = get_ints(melody1)
    ints2 = get_ints(melody2)

    # Check Transposition
    # There must be a constant shift k such that ints2[i] = (ints1[i] + k) % 12 for all i
    is_transposition = True
    if l > 0:
        k = (ints2[0] - ints1[0]) % 12
        for i in range(l):
            if (ints1[i] + k) % 12 != ints2[i]:
                is_transposition = False
                break
    else:
        is_transposition = True

    if is_transposition:
        print("Transposition")
        return

    # Check Retrograde
    # ints2 should be the reverse of ints1
    is_retrograde = True
    for i in range(l):
        if ints2[i] != ints1[l - 1 - i]:
            is_retrograde = False
            break
    if is_retrograde:
        print("Retrograde")
        return

    # Check Inversion
    # First note stays same. For i > 0, interval from first note is negated.
    # interval1[i] = ints1[i] - ints1[0]
    # interval2[i] = ints2[i] - ints2[0] (which should equal ints1[0] since first note doesn't change)
    # Condition: ints2[0] == ints1[0] AND (ints2[i] - ints2[0]) == -(ints1[i] - ints1[0]) mod 12
    is_inversion = True
    if l > 0:
        if ints2[0] != ints1[0]:
            is_inversion = False
        else:
            first_note = ints1[0]
            for i in range(1, l):
                interval1 = (ints1[i] - first_note) % 12
                interval2 = (ints2[i] - first_note) % 12
                if interval2 != (-interval1) % 12:
                    is_inversion = False
                    break
    else:
        is_inversion = True

    if is_inversion:
        print("Inversion")
        return

    print("Nonsense")

if __name__ == "__main__":
    solve()