import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    m = int(input_data[0])
    n = int(input_data[1])
    
    # We need to calculate E[max] = sum_{k=1}^{m} P(max >= k)
    # P(max >= k) = 1 - P(max < k) = 1 - P(all rolls < k)
    # P(all rolls < k) = P(roll <= k-1)^n = ((k-1)/m)^n
    
    # So E[max] = sum_{k=1}^{m} (1 - ((k-1)/m)^n)
    # Let j = k-1, then j goes from 0 to m-1
    # E[max] = sum_{j=0}^{m-1} (1 - (j/m)^n)
    #        = m - sum_{j=0}^{m-1} (j/m)^n
    # Note: when j=0, term is 0. So we can sum from j=1 to m-1.
    
    total = 0.0
    for j in range(1, m):
        term = (j / m) ** n
        total += term
    
    result = m - total
    print(f"{result:.12f}")

if __name__ == "__main__":
    solve()