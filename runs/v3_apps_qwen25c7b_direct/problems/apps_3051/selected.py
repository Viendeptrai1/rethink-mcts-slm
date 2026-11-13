import sys
from typing import List, Tuple

def calculate_missed_fogs(fogs: List[Tuple[int, int, int, int, int, int, int, int]]) -> int:
    missed = 0
    current_nets = []

    def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        intervals.sort()
        merged = []
        for start, end in intervals:
            if not merged or merged[-1][1] < start:
                merged.append((start, end))
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        return merged

    for m_i, d_i, l_i, r_i, h_i, delta_d_i, delta_x_i, delta_h_i in fogs:
        for k in range(m_i):
            day = d_i + k * delta_d_i
            l = l_i + k * delta_x_i
            r = r_i + k * delta_x_i
            h = h_i + k * delta_h_i
            new_nets = [(l, r)]
            for net_start, net_end in current_nets:
                if l >= net_end or r <= net_start:
                    continue
                if l > net_start:
                    new_nets.append((net_start, l))
                if r < net_end:
                    new_nets.append((r, net_end))
            current_nets = merge_intervals(new_nets)
            missed += sum(r - l for l, r in new_nets) * h

    return missed

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    
    fogs = []
    for _ in range(n):
        m_i = int(data[index])
        d_i = int(data[index + 1])
        l_i = int(data[index + 2])
        r_i = int(data[index + 3])
        h_i = int(data[index + 4])
        delta_d_i = int(data[index + 5])
        delta_x_i = int(data[index + 6])
        delta_h_i = int(data[index + 7])
        index += 8
        fogs.append((m_i, d_i, l_i, r_i, h_i, delta_d_i, delta_x_i, delta_h_i))
    
    result = calculate_missed_fogs(fogs)
    print(result)