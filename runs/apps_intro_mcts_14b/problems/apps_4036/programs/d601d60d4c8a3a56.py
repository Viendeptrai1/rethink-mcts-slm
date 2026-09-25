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
    
    # Distribute the remaining problems while maintaining the constraints
    i = 0
    while remaining_problems > 0:
        if i == k:
            i = 0
        if a[i] * 2 <= remaining_problems + a[i]:
            a[i] *= 2
            remaining_problems -= a[i]
        else:
            a[i] += remaining_problems
            remaining_problems = 0
        i += 1
    
    # Check if the sequence satisfies the constraints
    valid = True
    for i in range(1, k):
        if not (a[i] > a[i - 1] and a[i] <= 2 * a[i - 1]):
            valid = False
            break
    
    if valid:
        print("YES")
        print(" ".join(map(str, a)))
    else:
        print("NO")

if __name__ == "__main__":
    main()