def min_string(s, k):
    n = len(s)
    count_ones = s.count('1')
    if count_ones == 0 or count_ones == n:
        return s
    
    left = 0
    right = 0
    result = list(s)
    
    while right < n:
        if result[right] == '1':
            if right - left > k:
                break
            k -= (right - left)
            result[left], result[right] = result[right], result[left]
            left += 1
        right += 1
    
    return ''.join(result)

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        k = int(data[index + 1])
        s = data[index + 2]
        index += 3
        
        result = min_string(s, k)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    solve()