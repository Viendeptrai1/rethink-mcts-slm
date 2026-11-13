import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    a = []
    idx = 2
    for _ in range(n):
        a.append(int(data[idx]))
        idx += 1
    
    # Prefix XORs
    # p[i] = a[0] ^ ... ^ a[i-1], p[0] = 0
    # Segment XOR [l, r] (0-indexed) is p[r+1] ^ p[l]
    # We want p[r+1] ^ p[l] != 0, i.e., p[r+1] != p[l]
    
    p = [0] * (n + 1)
    curr = 0
    for i in range(n):
        curr ^= a[i]
        p[i+1] = curr
    
    # Count total segments: n*(n+1)//2
    # Subtract segments where p[r+1] == p[l]
    # For each value v, if it appears c times in p, then there are c*(c-1)//2 pairs (l, r+1) with same value
    # These correspond to segments with XOR 0.
    
    from collections import Counter
    cnt = Counter(p)
    
    zero_segments = 0
    for count in cnt.values():
        zero_segments += count * (count - 1) // 2
    
    total_segments = n * (n + 1) // 2
    result = total_segments - zero_segments
    
    print(result)

if __name__ == "__main__":
    solve()