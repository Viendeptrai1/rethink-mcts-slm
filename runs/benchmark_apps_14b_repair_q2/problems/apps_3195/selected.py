import sys

def main():
    import sys
    import math

    def read_int():
        return int(sys.stdin.readline().strip())

    def read_ints():
        return list(map(int, sys.stdin.readline().strip().split()))

    def read_str():
        return sys.stdin.readline().strip()

    def read_strs():
        return sys.stdin.readline().strip().split()

    Tg, Ty, Tr = read_ints()
    n = read_int()
    observations = []
    for _ in range(n):
        t, c = read_strs()
        observations.append((int(t), c))
    tq, cq = read_strs()
    tq = int(tq)

    # Calculate the total cycle length
    cycle_length = Tg + Ty + Tr

    # Find all possible start times T
    possible_T = set()
    for t, c in observations:
        if c == 'green':
            possible_T.add(t % cycle_length)
        elif c == 'yellow':
            possible_T.add((t - Tg) % cycle_length)
        elif c == 'red':
            possible_T.add((t - Tg - Ty) % cycle_length)

    # Count the number of valid start times
    valid_start_times = len(possible_T)

    # Calculate the probability for each color at time tq
    prob_green = 0
    prob_yellow = 0
    prob_red = 0

    for T in possible_T:
        if (tq - T) % cycle_length < Tg:
            prob_green += 1
        elif (tq - T) % cycle_length < Tg + Ty:
            prob_yellow += 1
        else:
            prob_red += 1

    prob_green /= valid_start_times
    prob_yellow /= valid_start_times
    prob_red /= valid_start_times

    # Return the probability for the queried color
    if cq == 'green':
        print(f"{prob_green:.3f}")
    elif cq == 'yellow':
        print(f"{prob_yellow:.3f}")
    elif cq == 'red':
        print(f"{prob_red:.3f}")

if __name__ == "__main__":
    main()