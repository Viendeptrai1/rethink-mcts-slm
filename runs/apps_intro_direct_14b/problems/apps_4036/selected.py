import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    if n < k or n > k * (1 + 2 ** (k - 1)):
        print("NO")
        return
    
    a = [1] * k
    remaining = n - k
    
    i = 0
    while remaining > 0:
        a[i] += 1
        remaining -= 1
        if i < k - 1 and a[i] * 2 <= a[i + 1]:
            i += 1
    
    print("YES")
    print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()