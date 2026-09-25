import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    if n < k:
        print("NO")
        return
    
    # Initialize the array with the minimum possible values
    a = [1] * k
    remaining_problems = n - k
    
    # Try to distribute the remaining problems while maintaining the constraints
    i = 0
    while remaining_problems > 0:
        if i == k - 1 or a[i] * 2 <= a[i + 1]:
            a[i] += 1
            remaining_problems -= 1
        else:
            i += 1
    
    # Check if the final array satisfies all conditions
    if sum(a) != n:
        print("NO")
    else:
        print("YES")
        print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()