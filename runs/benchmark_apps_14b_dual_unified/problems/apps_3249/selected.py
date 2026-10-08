import sys
import math

def calculate_area(x, y):
    n = len(x)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += x[i] * y[j]
        area -= y[i] * x[j]
    return abs(area) / 2.0

def find_bulkhead_positions(C, N, vertices):
    x = [vertices[i][0] for i in range(N)]
    y = [vertices[i][1] for i in range(N)]
    
    total_area = calculate_area(x, y)
    M = int(total_area // C)
    if total_area % C != 0:
        M += 1
    
    if M == 1:
        return 1, []
    
    target_area = total_area / M
    current_area = 0
    bulkhead_positions = []
    
    for i in range(1, N):
        dx = x[i] - x[i - 1]
        dy = y[i] - y[i - 1]
        segment_length = math.sqrt(dx**2 + dy**2)
        
        while current_area + segment_length * (y[i] + y[i - 1]) / 2 < target_area:
            t = (target_area - current_area) * 2 / (y[i] + y[i - 1])
            bulkhead_x = x[i - 1] + t * dx / segment_length
            bulkhead_positions.append(bulkhead_x)
            current_area = target_area
            target_area += total_area / M
        
        current_area += segment_length * (y[i] + y[i - 1]) / 2
    
    return M, bulkhead_positions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    C = int(data[0])
    N = int(data[1])
    vertices = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(N)]
    
    M, bulkhead_positions = find_bulkhead_positions(C, N, vertices)
    
    print(M)
    for pos in bulkhead_positions:
        print(f"{pos:.6f}")

if __name__ == "__main__":
    main()