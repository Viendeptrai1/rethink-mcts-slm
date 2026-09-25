import sys

def solve(a, b, c):
    # Find the smallest multiple of a that is >= b
    A = b // a * a
    if A < b:
        A += a
    
    # Find the smallest multiple of B that is >= c
    B = c // A * A
    if B < c:
        B += A
    
    # Calculate the number of operations needed
    res = (A - a) + (B - b)
    
    return res, A, B, B

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        c = int(data[index + 2])
        index += 3
        res, A, B, C = solve(a, b, c)
        results.append((res, A, B, C))
    
    for res, A, B, C in results:
        print(res)
        print(A, B, C)

if __name__ == "__main__":
    main()