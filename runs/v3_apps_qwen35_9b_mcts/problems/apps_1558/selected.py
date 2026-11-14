import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    r = int(next(iterator))
    avg = int(next(iterator))

    exams = []
    current_total = 0

    for _ in range(n):
        a = int(next(iterator))
        b = int(next(iterator))
        exams.append((b, a))
        current_total += a

    required_total = avg * n
    deficit = required_total - current_total

    if deficit <= 0:
        print(0)
        return

    exams.sort(key=lambda x: x[0])

    essays_needed = 0
    for b, a in exams:
        if deficit <= 0:
            break
        max_increase = r - a
        if max_increase <= 0:
            continue
        take = min(deficit, max_increase)
        essays_needed += take * b
        deficit -= take

    print(essays_needed)

if __name__ == "__main__":
    solve()