import sys

def min_lexicographic_string(n, k, s):
    s = list(s)
    count_ones = 0
    swaps = 0
    
    for i in range(n):
        if s[i] == '1':
            count_ones += 1
        else:
            if count_ones > 0:
                available_swaps = min(count_ones, k - swaps)
                swaps += available_swaps
                count_ones -= available_swaps
                s[i] = '1'
                if swaps == k:
                    break
    
    return ''.join(s)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    q = int(data[index])
    index += 1
    results = []
    
    for _ in range(q):
        n = int(data[index])
        k = int(data[index + 1])
        s = data[index + 2]
        index += 3
        result = min_lexicographic_string(n, k, s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()