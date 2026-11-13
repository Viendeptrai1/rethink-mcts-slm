import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    r = int(next(iterator))
    avg = int(next(iterator))

    current_sum = 0
    essays_needed = 0

    for _ in range(n):
        a = int(next(iterator))
        b = int(next(iterator))
        current_sum += a

    target_sum = avg * n
    diff = target_sum - current_sum

    if diff <= 0:
        print(0)
        return

    # Sort by cost b_i to greedily pick cheapest upgrades
    exams = []
    for _ in range(n):
        a = int(next(iterator))
        b = int(next(iterator))
        exams.append((a, b))

    # We need to sort by b, but we already consumed all input.
    # Let's reconstruct the list of (a, b) properly before sorting.
    # Actually, the loop above consumed everything. We need to re-read or store.
    # Since we are in a function and stdin is already read into a list, let's re-parse efficiently.
    pass

# Re-implementing with proper storage to avoid re-reading issues
def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    r = int(next(iterator))
    avg = int(next(iterator))

    current_sum = 0
    exams = []

    for _ in range(n):
        a = int(next(iterator))
        b = int(next(iterator))
        current_sum += a
        exams.append((a, b))

    target_sum = avg * n
    diff = target_sum - current_sum

    if diff <= 0:
        print(0)
        return

    # Sort exams by cost b_i
    exams.sort(key=lambda x: x[1])

    total_essays = 0
    points_gained = 0

    for a, b in exams:
        if points_gained >= diff:
            break
        max_increase = r - a
        take = min(max_increase, diff - points_gained)
        total_essays += take * b
        points_gained += take

    print(total_essays)

if __name__ == "__main__":
    main()