import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    if k == 1:
        if n > 0:
            print("YES")
            print(n)
        else:
            print("NO")
        return
    
    # Calculate the minimum number of problems Polycarp needs to solve
    min_problems = k * (k + 1) // 2
    
    if n < min_problems:
        print("NO")
        return
    
    # Initialize the array with the minimum possible values
    a = [0] * k
    current = 1
    total = 0
    
    for i in range(k):
        a[i] = current
        total += current
        current = min(current * 2, n - total)
    
    if total != n:
        print("NO")
    else:
        print("YES")
        print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()