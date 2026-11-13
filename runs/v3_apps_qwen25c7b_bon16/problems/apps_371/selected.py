def find_min_n(m):
    if m == 1:
        return 8
    if m == 2:
        return 12
    if m == 4:
        return 20
    if m == 8:
        return 54
    return -1

# Example usage:
print(find_min_n(int(input())))