def min_moves_to_make_divisible(t, test_cases):
    results = []
    for a, b in test_cases:
        if a % b == 0:
            results.append(0)
        else:
            remainder = a % b
            results.append(b - remainder)
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    test_cases = [(int(data[i]), int(data[i+1])) for i in range(1, 2*t, 2)]
    
    results = min_moves_to_make_divisible(t, test_cases)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()