import math
from sys import stdin

def max_fruits_on_slice(n, fruits):
    def dist(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    def can_slice(fruit, slope, intercept):
        x, y = fruit
        if abs(slope * x - y + intercept) <= 1:  # Distance formula adjusted for unit radius
            return True
        return False
    
    max_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = fruits[i]
            x2, y2 = fruits[j]
            if x1 == x2:  # Vertical line
                slope = float('inf')
                intercept = x1
            else:
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1
            count = sum(1 for fruit in fruits if can_slice(fruit, slope, intercept))
            max_count = max(max_count, count)
    return max_count

# Main function to read input and print the result
def main():
    n = int(stdin.readline().strip())
    fruits = [tuple(map(float, stdin.readline().strip().split())) for _ in range(n)]
    result = max_fruits_on_slice(n, fruits)
    print(result)

if __name__ == "__main__":
    main()