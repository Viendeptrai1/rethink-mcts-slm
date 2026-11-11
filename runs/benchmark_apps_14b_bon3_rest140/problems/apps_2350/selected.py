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
        
        # The number of steps to the right is (y2 - y1)
        # The number of steps down is (x2 - x1)
        steps_right = y2 - y1
        steps_down = x2 - x1
        
        # The total number of paths is C(steps_right + steps_down, steps_right)
        total_paths = math.comb(steps_right + steps_down, steps_right)
        
        # The minimum sum is the sum of the smallest numbers in the path
        min_sum = sum(range(1, steps_right + 1)) + sum(range(1, steps_down + 1))
        
        # The maximum sum is the sum of the largest numbers in the path
        max_sum = sum(range(y1, y1 + steps_right)) + sum(range(x1, x1 + steps_down))
        
        # The difference between consecutive sums is always 1
        # Therefore, the number of distinct sums is max_sum - min_sum + 1
        distinct_sums = max_sum - min_sum + 1
        
        return distinct_sums

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