import sys

def main():
    import sys
    import math

    def read_ints():
        return list(map(int, sys.stdin.readline().split()))

    def read_line():
        return sys.stdin.readline().strip()

    Tg, Ty, Tr = read_ints()
    n = read_ints()[0]
    observations = [read_line().split() for _ in range(n)]
    tq, cq = read_line().split()
    tq = int(tq)

    # Convert observations to a list of tuples (time, color)
    observations = [(int(t), c) for t, c in observations]

    # Calculate the total cycle length
    cycle_length = Tg + Ty + Tr

    # Find the possible start times T
    possible_T = []
    for t, c in observations:
        if c == 'green':
            # T must be such that t % cycle_length is in [0, Tg)
            possible_T.append((t % cycle_length, Tg))
        elif c == 'yellow':
            # T must be such that t % cycle_length is in [Tg, Tg + Ty)
            possible_T.append((t % cycle_length, Tg + Ty))
        else:  # c == 'red'
            # T must be such that t % cycle_length is in [Tg + Ty, Tg + Ty + Tr)
            possible_T.append((t % cycle_length, Tg + Ty + Tr))

    # Find the intersection of all possible T intervals
    min_start = float('inf')
    max_end = float('-inf')
    for start, end in possible_T:
        min_start = min(min_start, start)
        max_end = max(max_end, end)

    # If there is no intersection, the probability is 0
    if min_start >= max_end:
        print(0)
        return

    # Calculate the probability
    if cq == 'green':
        interval_length = Tg
    elif cq == 'yellow':
        interval_length = Ty
    else:  # cq == 'red'
        interval_length = Tr

    # Adjust the interval based on the intersection
    interval_start = max(min_start, tq % cycle_length)
    interval_end = min(max_end, (tq % cycle_length) + interval_length)

    if interval_start >= interval_end:
        print(0)
    else:
        probability = (interval_end - interval_start) / (max_end - min_start)
        print(f"{probability:.3f}")

if __name__ == "__main__":
    main()