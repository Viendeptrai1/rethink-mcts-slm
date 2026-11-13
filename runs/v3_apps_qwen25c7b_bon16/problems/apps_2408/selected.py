from itertools import combinations

def count_intersecting_wires(points):
    def are_intersecting(p1, p2, p3, p4):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            elif val > 0:
                return 1
            else:
                return 2
        
        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        if o1 != o2 and o3 != o4:
            return True
        return False
    
    count = 0
    for p1, p2, p3, p4 in combinations(points, 4):
        if are_intersecting(p1, p2, p3, p4):
            count += 1
    return count

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
points = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(n)]
print(count_intersecting_wires(points))