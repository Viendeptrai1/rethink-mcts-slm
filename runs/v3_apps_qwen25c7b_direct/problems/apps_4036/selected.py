def solve_polycarp_problems(n, k):
    if n < k or n > 2 * k * (k - 1) // 2:
        return "NO"
    
    # Initialize the array with the minimum possible values
    a = [1] * k
    remaining = n - k
    
    # Distribute the remaining problems while maintaining the constraints
    for i in range(k - 1):
        add = min(remaining, a[i], k - i - 1)
        a[i] += add
        remaining -= add
    
    # Check if we have enough problems left to distribute
    if remaining > 0:
        return "NO"
    
    return "YES\n" + " ".join(map(str, a))

# Example usage:
# print(solve_polycarp_problems(26, 6))
# print(solve_polycarp_problems(8, 3))
# print(solve_polycarp_problems(1, 1))
# print(solve_polycarp_problems(9, 4))