import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    if n < k or n > k * (2 ** (k - 1)):
        print("NO")
        return
    
    a = [1] * k
    remaining = n - k
    
    for i in range(k):
        max_possible = min(remaining, 2 * a[i] - a[i])
        a[i] += max_possible
        remaining -= max_possible
        if remaining == 0:
            break
    
    print("YES")
    print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()