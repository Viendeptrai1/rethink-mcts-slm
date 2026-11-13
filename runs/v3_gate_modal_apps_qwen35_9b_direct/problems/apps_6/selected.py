import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    t = int(data[idx])
    idx += 1
    
    results = []
    
    for _ in range(t):
        n = int(data[idx])
        x = int(data[idx+1])
        idx += 2
        
        blows = []
        max_d = 0
        min_net = float('inf')
        
        for _ in range(n):
            d = int(data[idx])
            h = int(data[idx+1])
            idx += 2
            blows.append((d, h))
            if d > max_d:
                max_d = d
            net = d - h
            if net < min_net:
                min_net = net
        
        if max_d >= x:
            results.append(1)
            continue
        
        if min_net >= 0:
            results.append(-1)
            continue
        
        # We need to reduce heads using the most efficient blow (min_net)
        # until the remaining heads can be cut off by the strongest blow (max_d)
        # Number of full cycles needed:
        # After k cycles, heads = x + k * min_net
        # We need x + k * min_net <= max_d
        # k * min_net <= max_d - x
        # k >= (max_d - x) / min_net (since min_net is negative, dividing flips inequality if we were careful, but let's just use math)
        # Actually: current_heads = x + k * min_net
        # We want current_heads <= max_d
        # k * min_net <= max_d - x
        # Since min_net < 0, dividing by it reverses inequality:
        # k >= (max_d - x) / min_net
        # But (max_d - x) is positive (since max_d < x initially) and min_net is negative, so RHS is negative.
        # Wait, logic check:
        # x = 10, max_d = 6, min_net = -3 (d=3, h=6)
        # k=0: 10 > 6
        # k=1: 10 - 3 = 7 > 6
        # k=2: 7 - 3 = 4 <= 6 -> OK
        # Formula: k >= (x - max_d) / (-min_net) ?
        # Let's derive properly:
        # heads_after_k = x + k * min_net
        # We need heads_after_k <= max_d
        # x + k * min_net <= max_d
        # k * min_net <= max_d - x
        # Since min_net is negative, let min_net = -p where p > 0
        # -k * p <= max_d - x
        # k * p >= x - max_d
        # k >= (x - max_d) / p
        # k = ceil((x - max_d) / p)
        
        p = -min_net
        needed_cycles = (x - max_d + p - 1) // p
        
        total_blows = needed_cycles + 1
        results.append(total_blows)

    for res in results:
        print(res)

if __name__ == '__main__':
    solve()