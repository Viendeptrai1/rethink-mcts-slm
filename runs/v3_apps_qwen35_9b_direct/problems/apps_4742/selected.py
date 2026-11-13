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
        return

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_to_idx = {note: i for i, note in enumerate(notes)}

    def get_idx(note):
        return note_to_idx[note]

    def is_transposition(m1, m2):
        if len(m1) != len(m2):
            return False
        diff = get_idx(m2[0]) - get_idx(m1[0])
        for i in range(1, len(m1)):
            expected = (get_idx(m1[i]) + diff) % 12
            if get_idx(m2[i]) != expected:
                return False
        return True

    def is_retrograde(m1, m2):
        if len(m1) != len(m2):
            return False
        return m1 == list(reversed(m2))

    def is_inversion(m1, m2):
        if len(m1) != len(m2):
            return False
        first_note_idx = get_idx(m1[0])
        if get_idx(m2[0]) != first_note_idx:
            return False
        for i in range(1, len(m1)):
            original_interval = get_idx(m1[i]) - first_note_idx
            inverted_interval = -original_interval
            expected_idx = (first_note_idx + inverted_interval) % 12
            if get_idx(m2[i]) != expected_idx:
                return False
        return True

    if is_transposition(melody1, melody2):
        print("Transposition")
    elif is_retrograde(melody1, melody2):
        print("Retrograde")
    elif is_inversion(melody1, melody2):
        print("Inversion")
    else:
        print("Nonsense")

if __name__ == "__main__":
    solve()