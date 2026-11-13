def solve():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B, C = map(int, data.split())
    
    # Check if there exists a multiple of A that is congruent to C modulo B
    # This is equivalent to checking if A and B are coprime
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    
    if gcd(A, B) == 1:
        print("YES")
    else:
        print("NO")