import sys
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def point_to_line_distance(point, line_point1, line_point2):
    x0, y0 = point
    x1, y1 = line_point1
    x2, y2 = line_point2
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = distance(line_point1, line_point2)
    return numerator / denominator

def max_fruits_sliced(fruits):
    n = len(fruits)
    max_count = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            count = 0
            for fruit in fruits:
                if point_to_line_distance(fruit, fruits[i], fruits[j]) <= 1.0:
                    count += 1
            max_count = max(max_count, count)
    
    return max_count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    fruits = []
    index = 1
    for _ in range(n):
        x = float(data[index])
        y = float(data[index + 1])
        fruits.append((x, y))
        index += 2
    
    result = max_fruits_sliced(fruits)
    print(result)

if __name__ == "__main__":
    main()