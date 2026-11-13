def solve_problems(n, k):
    if n < k:
        print("NO")
        return
    
    a = [0] * k
    remaining_problems = n
    
    for i in range(k):
        if i == 0:
            a[i] = 1
        else:
            a[i] = min(remaining_problems - (k - i - 1), 2 * a[i - 1])
            if a[i] < a[i - 1] + 1:
                a[i] = a[i - 1] + 1
        
        remaining_problems -= a[i]
    
    if remaining_problems != 0:
        print("NO")
    else:
        print("YES")
        print(*a)

# Read input
n, k = map(int, input().split())
solve_problems(n, k)