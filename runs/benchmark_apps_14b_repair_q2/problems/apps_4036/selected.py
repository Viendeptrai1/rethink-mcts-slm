import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    if n < k or n > k * (k + 1) // 2:
        print("NO")
        return
    
    a = [0] * k
    remaining = n
    
    for i in range(k):
        a[i] = max(1, remaining - (k - i - 1))
        remaining -= a[i]
    
    if remaining != 0:
        print("NO")
        return
    
    for i in range(1, k):
        if a[i] <= a[i - 1] or a[i] > 2 * a[i - 1]:
            print("NO")
            return
    
    print("YES")
    print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()