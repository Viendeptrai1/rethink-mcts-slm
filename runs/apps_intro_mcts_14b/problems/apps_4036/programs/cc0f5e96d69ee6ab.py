import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    # Check if it's possible to solve n problems in k days
    if k == 1:
        if n == 1:
            print("YES")
            print(1)
        else:
            print("NO")
        return
    
    # Calculate the minimum number of problems Polycarp can solve in k days
    min_problems = 0
    current_problems = 1
    for i in range(k):
        min_problems += current_problems
        current_problems *= 2
    
    if min_problems > n:
        print("NO")
        return
    
    # Construct the array a
    a = []
    current_problems = 1
    remaining_problems = n
    for i in range(k - 1):
        a.append(current_problems)
        remaining_problems -= current_problems
        current_problems *= 2
    
    # The last day should have enough problems to make the total n
    if remaining_problems >= current_problems and remaining_problems <= 2 * current_problems:
        a.append(remaining_problems)
        print("YES")
        print(" ".join(map(str, a)))
    else:
        print("NO")

if __name__ == "__main__":
    main()