import sys
from itertools import combinations

def max_fruits_sliced(fruits):
    def distance(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def can_slice(line, fruit):
        x1, y1 = line[0]
        x2, y2 = line[1]
        px, py = fruit
        d = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / distance((x1, y1), (x2, y2))
        return d <= 1

    max_count = 0
    for line in combinations(fruits, 2):
        count = sum(can_slice(line, fruit) for fruit in fruits)
        max_count = max(max_count, count)
    
    return max_count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    fruits = [(float(data[2*i+1]), float(data[2*i+2])) for i in range(n)]
    result = max_fruits_sliced(fruits)
    print(result)