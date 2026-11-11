import sys
from typing import List

def main():
    import sys
    import bisect
    
    def check_self_intersections(n: int, points: List[int]) -> str:
        # Sort points by their x-coordinates
        points.sort()
        
        # Active intervals to keep track of semi-circles
        active_intervals = []
        
        for i in range(1, n):
            x1, x2 = points[i-1], points[i]
            center = (x1 + x2) / 2
            radius = abs(x2 - x1) / 2
            
            # Check for intersection with active intervals
            left_edge = center - radius
            right_edge = center + radius
            
            # Find the position to insert the current interval
            pos = bisect.bisect_left(active_intervals, left_edge)
            
            # Check if the current interval overlaps with any active interval
            if pos < len(active_intervals) and active_intervals[pos] < right_edge:
                return "yes"
            
            # Add the current interval to the active list
            active_intervals.insert(pos, right_edge)
        
        return "no"
    
    # Read input
    n = int(sys.stdin.readline().strip())
    points = list(map(int, sys.stdin.readline().strip().split()))
    
    # Output the result
    print(check_self_intersections(n, points))

if __name__ == "__main__":
    main()