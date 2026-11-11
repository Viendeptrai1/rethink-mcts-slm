import sys

def min_lexicographic_string(n, k, s):
    s = list(s)
    zeros = []
    
    # Collect all positions of '0'
    for i in range(n):
        if s[i] == '0':
            zeros.append(i)
    
    zero_index = 0
    moves = 0
    
    # Try to bring the nearest '0' to the front within the allowed number of moves
    for i in range(n):
        if s[i] == '1':
            while zero_index < len(zeros) and zeros[zero_index] <= i and moves + (i - zeros[zero_index]) <= k:
                moves += (i - zeros[zero_index])
                s[i], s[zeros[zero_index]] = s[zeros[zero_index]], s[i]
                zero_index += 1
            if moves >= k:
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