def calculate_different_sums(t, test_cases):
    from collections import defaultdict
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    results = []
    for x1, y1, x2, y2 in test_cases:
        dx, dy = x2 - x1, y2 - y1
        g = gcd(dx, dy)
        
        # The number of different sums is (dx + dy - g + 1)
        results.append(dx + dy - g + 1)
    
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    test_cases = []
    index = 1
    for _ in range(t):
        x1 = int(data[index])
        y1 = int(data[index + 1])
        x2 = int(data[index + 2])
        y2 = int(data[index + 3])
        test_cases.append((x1, y1, x2, y2))
        index += 4
    
    results = calculate_different_sums(t, test_cases)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()