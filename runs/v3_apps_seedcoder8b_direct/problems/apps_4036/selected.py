def solve_problems(n, k):
    if k == 1:
        if n == 1:
            print("YES")
            print(1)
        else:
            print("NO")
        return

    # Start with the minimum possible value for the first day
    a = [1] * k
    n -= k

    # Distribute the remaining problems
    for i in range(k - 1, 0, -1):
        if n <= 0:
            break
        # Calculate the maximum number of problems we can solve on day i
        max_problems = min(2 * a[i], n + a[i])
        # Calculate the minimum number of problems we need to solve on day i
        min_problems = a[i - 1] + 1
        # Solve as many problems as possible on day i
        a[i] += min(max_problems - a[i], n)
        n -= (a[i] - min_problems)

    if n == 0:
        print("YES")
        print(*a)
    else:
        print("NO")

# Read input
n, k = map(int, input().split())
solve_problems(n, k)