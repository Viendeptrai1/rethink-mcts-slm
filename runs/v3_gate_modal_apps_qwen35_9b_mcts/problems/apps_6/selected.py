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
        
        max_d = 0
        max_net = 0
        
        for _ in range(n):
            d = int(data[idx])
            h = int(data[idx+1])
            idx += 2
            
            if d > max_d:
                max_d = d
            net = d - h
            if net > max_net:
                max_net = net
        
        if max_net <= 0:
            if max_d >= x:
                results.append(1)
            else:
                results.append(-1)
        else:
            # We need to reduce x to <= max_d using net reduction
            # Number of full cycles needed: ceil((x - max_d) / max_net)
            # If x <= max_d, we need 0 cycles, then 1 final blow
            if x <= max_d:
                results.append(1)
            else:
                diff = x - max_d
                cycles = (diff + max_net - 1) // max_net
                results.append(cycles + 1)
    
    for res in results:
        print(res)

if __name__ == "__main__":
    solve()