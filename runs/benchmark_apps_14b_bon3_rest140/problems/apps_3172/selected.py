import sys
from math import sqrt

def max_fruits_sliced(n, fruits):
    def distance(p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    def can_slice(fruit, line):
        x, y = fruit
        a, b, c = line
        # Distance from point (x, y) to line ax + by + c = 0
        dist = abs(a * x + b * y + c) / sqrt(a * a + b * b)
        return dist <= 1
    
    max_slices = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Define the line passing through fruits[i] and fruits[j]
            x1, y1 = fruits[i]
            x2, y2 = fruits[j]
            if x1 == x2:  # Vertical line
                a, b, c = 1, 0, -x1
            else:
                m = (y2 - y1) / (x2 - x1)
                a, b, c = m, -1, y1 - m * x1
            
            count = sum(can_slice(fruit, (a, b, c)) for fruit in fruits)
            max_slices = max(max_slices, count)
    
    return max_slices

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    fruits = [(float(data[2*i+1]), float(data[2*i+2])) for i in range(n)]
    
    result = max_fruits_sliced(n, fruits)
    print(result)

if __name__ == "__main__":
    main()