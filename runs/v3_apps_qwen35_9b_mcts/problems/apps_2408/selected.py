import sys
from math import gcd

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    
    points = []
    for _ in range(n):
        x = int(next(iterator))
        y = int(next(iterator))
        points.append((x, y))
    
    # Normalize a line represented by ax + by + c = 0
    # We will store lines as a tuple (a, b, c) normalized such that:
    # 1. gcd(|a|, |b|, |c|) == 1
    # 2. The first non-zero among (a, b) is positive
    # If a=0 and b=0, it's invalid (shouldn't happen with distinct points)
    
    def normalize_line(a, b, c):
        g = gcd(a, gcd(b, c))
        a //= g
        b //= g
        c //= g
        
        if a < 0 or (a == 0 and b < 0):
            a = -a
            b = -b
            c = -c
        return (a, b, c)
    
    lines = set()
    
    # Generate all unique lines
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Line equation: (y2 - y1)x - (x2 - x1)y + (x2*y1 - y2*x1) = 0
            # A = y2 - y1
            # B = -(x2 - x1) = x1 - x2
            # C = x2*y1 - y2*x1
            A = y2 - y1
            B = x1 - x2
            C = x2 * y1 - y2 * x1
            
            norm = normalize_line(A, B, C)
            lines.add(norm)
    
    # Count intersecting pairs of lines
    # Two lines intersect if they are not parallel.
    # Lines are parallel if their normal vectors (a, b) are proportional.
    # Since we normalized, two lines are parallel if (a1, b1) == (a2, b2).
    # They are the same line if (a1, b1, c1) == (a2, b2, c2).
    # We only care about distinct lines.
    
    # Group lines by their direction (a, b)
    from collections import defaultdict
    direction_groups = defaultdict(list)
    
    for line in lines:
        a, b, c = line
        direction_groups[(a, b)].append(line)
    
    total_intersecting = 0
    
    # Iterate over all pairs of direction groups
    group_list = list(direction_groups.items())
    for i in range(len(group_list)):
        for j in range(i + 1, len(group_list)):
            dir1, lines1 = group_list[i]
            dir2, lines2 = group_list[j]
            
            # Since directions are different, all lines in group1 intersect all lines in group2
            total_intersecting += len(lines1) * len(lines2)
    
    print(total_intersecting)

if __name__ == "__main__":
    solve()