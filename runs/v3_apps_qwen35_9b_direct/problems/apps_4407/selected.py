import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = int(data[1])
    
    a = []
    idx = 2
    for _ in range(n):
        a.append(int(data[idx]))
        idx += 1
    
    queries = []
    for _ in range(q):
        queries.append(int(data[idx]))
        idx += 1
    
    # Count available coins for each power of 2
    # Since a_i <= 2*10^9, max power is around 30 (2^30 > 10^9)
    # We'll use an array of size 32 to cover up to 2^31
    count = [0] * 32
    
    for val in a:
        # Calculate log2(val)
        # Since val is guaranteed to be a power of 2, we can use bit_length - 1
        d = val.bit_length() - 1
        if d < 32:
            count[d] += 1
    
    results = []
    
    for b in queries:
        if b == 0:
            results.append(0)
            continue
            
        possible = True
        current_val = 0
        coins_used = 0
        
        # Try to form b from largest powers to smallest
        # We iterate from bit 30 down to 0
        for d in range(30, -1, -1):
            if (b >> d) & 1:
                # We need a coin of value 2^d
                if count[d] > 0:
                    count[d] -= 1
                    current_val += (1 << d)
                    coins_used += 1
                else:
                    possible = False
                    break
        
        if possible and current_val == b:
            results.append(coins_used)
        else:
            results.append(-1)
    
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()