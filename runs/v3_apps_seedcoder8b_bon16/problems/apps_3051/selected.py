import sys

def count_missed_fogs(n, fogs):
    missed_fogs = 0
    settled_fogs = []

    for fog in fogs:
        mi, di, li, ri, hi, ddi, dxi, dhi = fog
        for k in range(mi):
            x = li + k * dxi
            y = hi + k * dhi
            d = di + k * ddi
            settled_fogs.append((x, y, d))

    settled_fogs.sort(key=lambda x: x[2])

    current_day = 0
    nets = []

    for fog in settled_fogs:
        x, y, day = fog

        while current_day < day:
            current_day += 1
            new_nets = []
            for net in nets:
                new_nets.append(net)
            nets = new_nets

        missed = True
        for net in nets:
            if net[0] <= x <= net[2] and net[1] <= y <= net[3]:
                missed = False
                break

        if missed:
            nets.append((x, 0, x, y))
            missed_fogs += 1

    return missed_fogs

def main():
    n = int(input())
    fogs = []
    for _ in range(n):
        fog = list(map(int, input().split()))
        fogs.append(fog)

    result = count_missed_fogs(n, fogs)
    print(result)

if __name__ == "__main__":
    main()