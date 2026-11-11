import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    # Check if it's possible to solve n problems in k days
    if n < k or n > (2**k - 1):
        print("NO")
        return
    
    # Initialize the list of problems solved per day
    a = [0] * k
    current_problems = 1
    total_problems = 0
    
    for i in range(k):
        a[i] = current_problems
        total_problems += current_problems
        if total_problems >= n:
            break
        current_problems = min(2 * current_problems, n - total_problems)
    
    if total_problems != n:
        print("NO")
    else:
        print("YES")
        print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()