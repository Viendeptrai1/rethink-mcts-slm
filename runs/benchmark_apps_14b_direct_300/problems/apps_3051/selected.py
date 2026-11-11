import sys
from typing import List, Tuple

def count_missed_fogs(n: int, fogs: List[Tuple[int, int, int, int, int, int, int, int]]) -> int:
    def get_fog_rectangles(fog):
        mi, di, li, ri, hi, delta_di, delta_xi, delta_hi = fog
        rectangles = []
        for k in range(mi):
            day = di + k * delta_di
            left = li + k * delta_xi
            right = ri + k * delta_xi
            height = hi + k * delta_hi
            rectangles.append((day, left, right, height))
        return rectangles

    all_rectangles = []
    for fog in fogs:
        all_rectangles.extend(get_fog_rectangles(fog))

    all_rectangles.sort()

    def is_covered(rect, covered_intervals):
        left, right, height = rect
        for interval in covered_intervals:
            if interval[0] <= left and right <= interval[1]:
                return True
        return False

    def add_patch(covered_intervals, rect):
        left, right, height = rect
        new_intervals = []
        added = False
        for interval in covered_intervals:
            if interval[1] < left:
                new_intervals.append(interval)
            elif right < interval[0]:
                if not added:
                    new_intervals.append((left, right))
                    added = True
                new_intervals.append(interval)
            else:
                new_left = min(left, interval[0])
                new_right = max(right, interval[1])
                new_intervals.append((new_left, new_right))
        if not added:
            new_intervals.append((left, right))
        return new_intervals

    covered_intervals = []
    missed_count = 0

    for day, left, right, height in all_rectangles:
        if not is_covered((left, right, height), covered_intervals):
            missed_count += 1
        covered_intervals = add_patch(covered_intervals, (left, right, height))

    return missed_count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    fogs = []
    index = 1
    for _ in range(n):
        mi = int(data[index])
        di = int(data[index + 1])
        li = int(data[index + 2])
        ri = int(data[index + 3])
        hi = int(data[index + 4])
        delta_di = int(data[index + 5])
        delta_xi = int(data[index + 6])
        delta_hi = int(data[index + 7])
        fogs.append((mi, di, li, ri, hi, delta_di, delta_xi, delta_hi))
        index += 8
    
    result = count_missed_fogs(n, fogs)
    print(result)

if __name__ == "__main__":
    main()