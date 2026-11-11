import sys

def main():
    import sys
    import math
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return a * b // gcd(a, b)
    
    def count_distinct_sums(x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return 1
        
        # Number of steps to the right and down
        right_steps = y2 - y1
        down_steps = x2 - x1
        
        # Total number of steps
        total_steps = right_steps + down_steps
        
        # The minimum and maximum possible sums
        min_sum = (x1 + y1 - 1) * total_steps // 2 + (total_steps + 1) * (total_steps + 2) // 2
        max_sum = (x2 + y2 - 1) * total_steps // 2 + (total_steps + 1) * (total_steps + 2) // 2
        
        # The number of distinct sums is the number of integers in the range [min_sum, max_sum]
        return max_sum - min_sum + 1
    
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