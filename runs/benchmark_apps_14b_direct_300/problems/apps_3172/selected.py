import sys
from typing import List, Tuple

def max_fruits_sliced(n: int, fruits: List[Tuple[float, float]]) -> int:
    def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def can_slice(fruit: Tuple[float, float], p1: Tuple[float, float], p2: Tuple[float, float]) -> bool:
        d1 = distance(fruit, p1)
        d2 = distance(fruit, p2)
        d = distance(p1, p2)
        return abs(d1**2 + d2**2 - d**2) <= 1e-6 or min(d1, d2) <= 1

    max_slices = 0
    for i in range(n):
        for j in range(i + 1, n):
            current_slices = 0
            for fruit in fruits:
                if can_slice(fruit, fruits[i], fruits[j]):
                    current_slices += 1
            max_slices = max(max_slices, current_slices)
    return max_slices

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