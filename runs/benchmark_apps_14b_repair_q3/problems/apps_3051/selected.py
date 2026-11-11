import sys
from typing import List, Tuple

def read_input() -> Tuple[int, List[Tuple[int, int, int, int, int, int, int, int]]]:
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
    
    return n, fogs

def compute_missed_fogs(n: int, fogs: List[Tuple[int, int, int, int, int, int, int, int]]) -> int:
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
    
    all_rectangles.sort(key=lambda x: x[0])
    
    missed_count = 0
    current_nets = []
    
    for day, left, right, height in all_rectangles:
        # Remove outdated nets
        current_nets = [net for net in current_nets if net[0] >= day]
        
        # Check if the current fog is missed
        missed = True
        for net_day, net_right, net_height in current_nets:
            if net_right >= right and net_height >= height:
                missed = False
                break
        
        if missed:
            missed_count += 1
            current_nets.append((day, right, height))
    
    return missed_count

def main():
    n, fogs = read_input()
    result = compute_missed_fogs(n, fogs)
    print(result)

if __name__ == "__main__":
    main()