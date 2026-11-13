def remaining_water(A, B, C):
    return max(0, C - (A - B))

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    result = remaining_water(A, B, C)
    print(result)