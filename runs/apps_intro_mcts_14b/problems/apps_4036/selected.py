import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    if k == 1:
        if n == 1:
            print("YES")
            print("1")
        else:
            print("NO")
        return
    
    # Check if it's possible to distribute n problems in k days
    if n < k or n > (2**k - 1):
        print("NO")
        return
    
    # Initialize the array with the minimum possible values
    a = [1] * k
    remaining = n - k
    
    # Distribute the remaining problems
    i = 0
    while remaining > 0:
        if i == k - 1 or a[i] * 2 > a[i + 1]:
            a[i] += min(remaining, a[i] * 2 - a[i])
            remaining -= min(remaining, a[i] * 2 - a[i])
        i += 1
    
    # Verify the solution
    if sum(a) != n:
        print("NO")
        return
    
    print("YES")
    print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()