import math
import sys
from heapq import heappush, heappop

def minimum_time_to_destination(x1, y1, x2, y2, v_max, t, wind1, wind2):
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def time_to_reach(x, y, vx, vy, dest_x, dest_y, v_max):
        dx = dest_x - x
        dy = dest_y - y
        dot_product = dx * vx + dy * vy
        if dot_product > 0:
            return float('inf')
        speed_required = math.sqrt(max(0, (dx**2 + dy**2) - dot_product**2))
        return (speed_required / v_max) if speed_required <= v_max else float('inf')
    
    def dijkstra(start_x, start_y, end_x, end_y):
        pq = []
        heappush(pq, (0, start_x, start_y))
        visited = set()
        
        while pq:
            current_time, x, y = heappop(pq)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            if math.isclose(x, end_x, abs_tol=1e-9) and math.isclose(y, end_y, abs_tol=1e-9):
                return current_time
            
            for vx, vy, wx, wy in [(wind1[0], wind1[1], wind2[0], wind2[1])]:
                new_x = x + current_time * wx
                new_y = y + current_time * wy
                travel_time = time_to_reach(new_x, new_y, wx, wy, end_x, end_y, v_max)
                if travel_time < float('inf'):
                    heappush(pq, (current_time + travel_time, new_x, new_y))
        
        return float('inf')
    
    return dijkstra(x1, y1, x2, y2)

def main():
    input = sys.stdin.read
    data = input().split()
    
    x1, y1, x2, y2 = map(int, data[:4])
    v_max, t = map(int, data[4:6])
    wind1 = tuple(map(int, data[6:8]))
    wind2 = tuple(map(int, data[8:10]))
    
    result = minimum_time_to_destination(x1, y1, x2, y2, v_max, t, wind1, wind2)
    print(result)

if __name__ == "__main__":
    main()