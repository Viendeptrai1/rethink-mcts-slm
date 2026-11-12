def check_records(test_cases):
    results = []
    for _ in range(test_cases):
        n = int(input())
        previous_p, previous_c = 0, 0
        valid = True
        for _ in range(n):
            p, c = map(int, input().split())
            if p < previous_p or c > previous_c or (c == previous_c and p != previous_p):
                valid = False
                break
            previous_p, previous_c = p, c
        results.append("YES" if valid else "NO")
    return results

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    index = 0
    def read_int():
        nonlocal index
        result = int(data[index])
        index += 1
        return result
    
    test_cases = read_int()
    results = check_records(test_cases)
    for result in results:
        print(result)