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
    for obs in observations:
        obs[0] = int(obs[0])

    # Calculate the total cycle length
    cycle_length = Tg + Ty + Tr

    # Determine the possible start times T
    possible_T = set()
    for t, c in observations:
        if c == 'green':
            possible_T.add((t % cycle_length) - Tg)
        elif c == 'yellow':
            possible_T.add((t % cycle_length) - Tg - Ty)
        elif c == 'red':
            possible_T.add((t % cycle_length) - Tg - Ty - Tr)

    # Filter out impossible start times
    valid_T = []
    for T in possible_T:
        valid = True
        for t, c in observations:
            light_time = (t - T) % cycle_length
            if c == 'green' and not (0 <= light_time < Tg):
                valid = False
                break
            elif c == 'yellow' and not (Tg <= light_time < Tg + Ty):
                valid = False
                break
            elif c == 'red' and not (Tg + Ty <= light_time < Tg + Ty + Tr):
                valid = False
                break
        if valid:
            valid_T.append(T)

    if not valid_T:
        print(0)
        return

    # Calculate the probability
    count = 0
    for T in valid_T:
        light_time = (tq - T) % cycle_length
        if cq == 'green' and 0 <= light_time < Tg:
            count += 1
        elif cq == 'yellow' and Tg <= light_time < Tg + Ty:
            count += 1
        elif cq == 'red' and Tg + Ty <= light_time < Tg + Ty + Tr:
            count += 1

    probability = count / len(valid_T)
    print(f"{probability:.3f}")

if __name__ == "__main__":
    main()