def mexican_wave(n, k, t):
    if t < k:
        return t + 1
    elif t < 2 * k:
        return k
    else:
        return n - (t - k)

# Example usage:
# print(mexican_wave(10, 5, 3))  # Output: 3
# print(mexican_wave(10, 5, 7))  # Output: 5
# print(mexican_wave(10, 5, 12)) # Output: 3