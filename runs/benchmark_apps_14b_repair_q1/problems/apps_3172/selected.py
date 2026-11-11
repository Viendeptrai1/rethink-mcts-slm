import sys
from math import sqrt

def max_fruits_sliced(n, fruits):
    def distance(p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    def is_on_line(p, line):
        x1, y1 = line[0]
        x2, y2 = line[1]
        x, y = p
        # Check if point lies on the line segment defined by x1,y1 and x2,y2
        if (x - x1) * (y2 - y1) == (y - y1) * (x2 - x1):
            # Check if point is within the bounds of the line segment
            if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
                return True
        return False
    
    def is_intersected(fruit, line):
        x, y = fruit
        x1, y1 = line[0]
        x2, y2 = line[1]
        # Calculate the perpendicular distance from the fruit center to the line
        numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        d = numerator / denominator
        # If the distance is less than or equal to the radius of the fruit, it's intersected
        return d <= 1
    
    max_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            line = (fruits[i], fruits[j])
            count = 0
            for fruit in fruits:
                if is_intersected(fruit, line):
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
    
    result = max_fruits_sliced(n, fruits)
    print(result)

if __name__ == "__main__":
    main()