import sys

def solve(n, k):
    if n < k or n > k * (2 ** (k - 1)):
        return "NO"
    
    a = [1] * k
    remaining = n - k
    
    for i in range(k - 1):
        max_possible = min(remaining, 2 * a[i] - a[i])
        a[i + 1] = a[i] + max_possible
        remaining -= max_possible
    
    return "YES", a

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    result = solve(n, k)
    
    if result == "NO":
        print("NO")
    else:
        print("YES")
        print(" ".join(map(str, result[1])))

if __name__ == "__main__":
    main()