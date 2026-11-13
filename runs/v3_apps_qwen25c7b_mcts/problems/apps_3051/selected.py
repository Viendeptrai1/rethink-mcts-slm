import sys
from typing import List, Tuple

def simulate_fog_catching(n: int, fogs: List[Tuple[int, int, int, int, int, int, int, int]]) -> int:
    missed_fogs = 0
    current_nets = []

    def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        intervals.sort()
        merged = []
        for interval in intervals:
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
        return merged

    for day in range(max(fog[1] for fog in fogs)):
        new_nets = []
        for fog in fogs:
            if day >= fog[1]:
                for k in range(fog[0]):
                    left = fog[2] + k * fog[6]
                    right = fog[3] + k * fog[6]
                    height = fog[4] + k * fog[7]
                    if height > 0:
                        new_nets.append((left, right))
        current_nets.extend(new_nets)
        current_nets = merge_intervals(current_nets)

        for fog in fogs:
            if day >= fog[1]:
                for k in range(fog[0]):
                    left = fog[2] + k * fog[6]
                    right = fog[3] + k * fog[6]
                    height = fog[4] + k * fog[7]
                    if height > 0:
                        found = False
                        for net in current_nets:
                            if left <= net[0] and net[1] <= right:
                                found = True
                                break
                        if not found:
                            missed_fogs += 1

    return missed_fogs

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    fogs = []
    index = 1
    for i in range(n):
        m_i = int(data[index])
        d_i = int(data[index + 1])
        l_i = int(data[index + 2])
        r_i = int(data[index + 3])
        h_i = int(data[index + 4])
        delta_d_i = int(data[index + 5])
        delta_x_i = int(data[index + 6])
        delta_h_i = int(data[index + 7])
        fogs.append((m_i, d_i, l_i, r_i, h_i, delta_d_i, delta_x_i, delta_h_i))
        index += 8

    result = simulate_fog_catching(n, fogs)
    print(result)