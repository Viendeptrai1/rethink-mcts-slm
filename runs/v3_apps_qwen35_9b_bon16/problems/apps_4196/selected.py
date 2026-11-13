import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:]))
    
    # Compute prefix GCDs
    prefix_gcd = [0] * n
    curr = 0
    for i in range(n):
        if i == 0:
            curr = a[i]
        else:
            curr = gcd(curr, a[i])
        prefix_gcd[i] = curr
    
    # Compute suffix GCDs
    suffix_gcd = [0] * n
    curr = 0
    for i in range(n - 1, -1, -1):
        if i == n - 1:
            curr = a[i]
        else:
            curr = gcd(curr, a[i])
        suffix_gcd[i] = curr
    
    # Try removing each element and compute GCD of the rest
    max_gcd = 0
    for i in range(n):
        if i == 0:
            g = suffix_gcd[1]
        elif i == n - 1:
            g = prefix_gcd[n - 2]
        else:
            g = gcd(prefix_gcd[i - 1], suffix_gcd[i + 1])
        
        if g > max_gcd:
            max_gcd = g
    
    # If n=2, we can choose any number, so the answer is max(a) if we could pick freely,
    # but we must replace one with something between 1 and 10^9.
    # Actually, if we remove one, the GCD of the remaining one is the number itself.
    # We can set the replaced number to be equal to that remaining number.
    # So for n=2, the answer is max(a[0], a[1]).
    # Our loop above handles this: if i=0, g = a[1]; if i=1, g = a[0].
    # Then we can set the replaced element to g, so GCD becomes g.
    # So the logic holds.
    
    print(max_gcd)

if __name__ == "__main__":
    solve()