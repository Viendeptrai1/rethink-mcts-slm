import sys
from typing import List, Tuple

def read_input() -> Tuple[int, List[Tuple[int, int, int, int, int, int, int, int]]]:
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    fogs = []
    index = 1
    for _ in range(n):
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
    
    return n, fogs

def get_fog_rectangles(fog: Tuple[int, int, int, int, int, int, int, int]) -> List[Tuple[int, int, int, int]]:
    m_i, d_i, l_i, r_i, h_i, delta_d_i, delta_x_i, delta_h_i = fog
    rectangles = []
    for k in range(m_i):
        day = d_i + k * delta_d_i
        left = l_i + k * delta_x_i
        right = r_i + k * delta_x_i
        height = h_i + k * delta_h_i
        rectangles.append((day, left, right, height))
    return rectangles

def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    intervals.sort()
    merged = []
    current_start, current_end = intervals[0]
    
    for start, end in intervals[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    
    merged.append((current_start, current_end))
    return merged

def calculate_missed_fogs(n: int, fogs: List[Tuple[int, int, int, int, int, int, int, int]]) -> int:
    from collections import defaultdict
    
    day_to_rectangles = defaultdict(list)
    
    for fog in fogs:
        rectangles = get_fog_rectangles(fog)
        for day, left, right, height in rectangles:
            day_to_rectangles[day].append((left, right, height))
    
    total_missed = 0
    current_nets = []
    
    for day in sorted(day_to_rectangles.keys()):
        rectangles = day_to_rectangles[day]
        
        # Sort rectangles by left boundary
        rectangles.sort(key=lambda x: x[0])
        
        # Merge overlapping intervals
        intervals = [(rect[0], rect[1]) for rect in rectangles]
        merged_intervals = merge_intervals(intervals)
        
        # Calculate missed fogs
        for left, right, height in rectangles:
            missed = True
            for net_left, net_right, net_height in current_nets:
                if left >= net_left and right <= net_right and height <= net_height:
                    missed = False
                    break
            if missed:
                total_missed += 1
        
        # Update current nets
        for left, right, height in rectangles:
            added = False
            for i, (net_left, net_right, net_height) in enumerate(current_nets):
                if left >= net_left and right <= net_right and height <= net_height:
                    added = True
                    break
                elif left <= net_left and right >= net_right and height >= net_height:
                    current_nets[i] = (left, right, height)
                    added = True
                    break
            if not added:
                current_nets.append((left, right, height))
    
    return total_missed

def main():
    n, fogs = read_input()
    result = calculate_missed_fogs(n, fogs)
    print(result)

if __name__ == "__main__":
    main()