def lexicographically_minimum_string(q, test_cases):
    results = []
    for n, k, s in test_cases:
        s = list(s)
        moves = 0
        for i in range(n):
            if moves >= k:
                break
            min_index = i
            for j in range(i + 1, min(n, i + k - moves + 1)):
                if s[j] < s[min_index]:
                    min_index = j
            if min_index != i:
                for j in range(min_index, i, -1):
                    s[j], s[j - 1] = s[j - 1], s[j]
                moves += min_index - i
        results.append(''.join(s))
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    index = 1
    test_cases = []
    for _ in range(q):
        n = int(data[index])
        k = int(data[index + 1])
        s = data[index + 2]
        test_cases.append((n, k, s))
        index += 3
    
    results = lexicographically_minimum_string(q, test_cases)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()