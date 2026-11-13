def min_moves_to_divisible(t, test_cases):
    results = []
    for a, b in test_cases:
        if a % b == 0:
            results.append(0)
        else:
            results.append(b - (a % b))
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    test_cases = []
    index = 1
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        test_cases.append((a, b))
        index += 2
    
    results = min_moves_to_divisible(t, test_cases)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()