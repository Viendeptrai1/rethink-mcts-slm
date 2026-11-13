import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    
    if n == 2:
        print(1)
        print(2)
    elif n == 3:
        print(1)
        print(3)
    else:
        # For n >= 4, we can use as many 2s as possible.
        # If n is even: n = 2 + 2 + ... + 2 (n/2 times)
        # If n is odd: n = 2 + 2 + ... + 2 + 3 (since n is odd, n-3 is even)
        # In both cases, the number of primes is maximized by using 2s mostly.
        # Actually, for odd n, we can do (n-3)/2 twos and one 3.
        # Total count = (n-3)/2 + 1 = (n-1)/2.
        # For even n, count = n/2.
        # Notice that for odd n, (n-1)/2 is the same as floor(n/2).
        # So in general, k = n // 2.
        
        k = n // 2
        print(k)
        if n % 2 == 0:
            print(" ".join(["2"] * k))
        else:
            # n is odd: print (k-1) twos and one 3
            twos = " ".join(["2"] * (k - 1))
            print(f"{twos} 3")

if __name__ == "__main__":
    solve()