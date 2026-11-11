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

    # Convert times to integers
    observations = [(int(t), c) for t, c in observations]

    # Function to determine the state of the light at time t
    def get_light_state(T, t):
        cycle_length = Tg + Ty + Tr
        t = (t - T) % cycle_length
        if t < Tg:
            return "green"
        elif t < Tg + Ty:
            return "yellow"
        else:
            return "red"

    # Find the common range for T
    common_T_start = float('inf')
    common_T_end = float('-inf')

    for i in range(n - 1):
        t1, c1 = observations[i]
        t2, c2 = observations[i + 1]
        if c1 == c2:
            continue

        if c1 == "green":
            if c2 == "yellow":
                T_start = t1
                T_end = t2
            elif c2 == "red":
                T_start = t1 - Tg
                T_end = t2 - Tg
        elif c1 == "yellow":
            if c2 == "green":
                T_start = t1 - Ty
                T_end = t2 - Ty
            elif c2 == "red":
                T_start = t1
                T_end = t2
        elif c1 == "red":
            if c2 == "green":
                T_start = t1 - Tr
                T_end = t2 - Tr
            elif c2 == "yellow":
                T_start = t1 - Tr - Ty
                T_end = t2 - Tr - Ty

        common_T_start = max(common_T_start, T_start)
        common_T_end = min(common_T_end, T_end)

    # Calculate the probability
    cycle_length = Tg + Ty + Tr
    if common_T_start > common_T_end:
        print(0)
        return

    valid_range = common_T_end - common_T_start + 1
    valid_cycles = math.ceil(valid_range / cycle_length)

    if cq == "green":
        green_duration = Tg
    elif cq == "yellow":
        green_duration = Ty
    else:
        green_duration = Tr

    probability = (valid_cycles * green_duration) / valid_range
    print(f"{probability:.3f}")

if __name__ == "__main__":
    main()