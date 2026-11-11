import sys
import math

def main():
    def count_distinct_sums(x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return 1
        
        # Calculate the number of steps
        steps = x2 - x1 + y2 - y1
        
        # Calculate the number of paths
        return math.comb(steps, x2 - x1)

    t = int(sys.stdin.readline())
    results = []
    
    for _ in range(t):
        x1, y1, x2, y2 = map(int, sys.stdin.readline().split())
        result = count_distinct_sums(x1, y1, x2, y2)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()