import sys
import math

def max_fruits_sliced(n, fruits):
    def angle(p1, p2):
        return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    
    max_count = 0
    for i in range(n):
        angles = set()
        for j in range(n):
            if i != j:
                ang = angle(fruits[i], fruits[j])
                angles.add(ang)
                angles.add(ang + math.pi)
        max_count = max(max_count, len(angles) // 2)
    
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