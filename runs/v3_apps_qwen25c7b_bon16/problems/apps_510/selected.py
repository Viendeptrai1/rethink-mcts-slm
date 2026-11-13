def min_performance_duration(a, b, c, d):
    # Ensure a <= b <= c for simplicity
    if a > b:
        a, b = b, a
    if a > c:
        a, c = c, a
    if b > c:
        b, c = c, b
    
    # Calculate the minimum shifts needed for each pair
    shifts_a_b = max(0, d - (b - a))
    shifts_b_c = max(0, d - (c - b))
    
    # The total minimum shifts required
    return shifts_a_b + shifts_b_c

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = list(map(int, input().split()))
    result = min_performance_duration(*data)
    print(result)