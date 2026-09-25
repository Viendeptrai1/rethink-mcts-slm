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
            print(1)
        else:
            print("NO")
        return
    
    # Initialize the array with the minimum possible values
    a = [1] * k
    total = k
    
    # Distribute the remaining problems
    i = 0
    while total < n:
        if i == k - 1:
            # If we can't add more problems to the last day, it's impossible
            print("NO")
            return
        # Double the problems for the next day
        a[i + 1] = min(a[i] * 2, n - total)
        total += a[i + 1]
        i += 1
    
    if total == n:
        print("YES")
        print(" ".join(map(str, a)))
    else:
        print("NO")

if __name__ == "__main__":
    main()