import sys

def solve_training_problems(n, k):
    if k == 1:
        if n == 1:
            print("YES")
            print(1)
        else:
            print("NO")
        return

    # Check if it's possible to distribute n problems over k days
    if n < k or n > 2 * k:
        print("NO")
        return

    # Calculate the minimum and maximum possible values for the first day
    min_first_day = (n + k - 1) // k
    max_first_day = min(2 * min_first_day, n - k + 1)

    # Try to find a valid distribution
    for first_day in range(max_first_day, min_first_day - 1, -1):
        remaining = n - first_day
        a = [first_day]
        valid = True

        for i in range(1, k):
            if remaining < i + 1 or remaining > 2 * (i + 1):
                valid = False
                break
            next_day = min(remaining - i, 2 * (i + 1))
            a.append(next_day)
            remaining -= next_day

        if valid:
            print("YES")
            print(*a)
            return

    print("NO")

# Read input
n, k = map(int, sys.stdin.readline().split())

# Solve the problem
solve_training_problems(n, k)