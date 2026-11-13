def min_rows_for_mirroring(n, m, a):
    # Check if the matrix can be mirrored to match the given matrix a
    def can_mirror_to(a):
        x = len(a)
        y = len(a[0])
        for i in range(x // 2):
            if a[i] != a[x - 1 - i]:
                return False
        return True
    
    # If the matrix can be mirrored directly, return 1
    if can_mirror_to(a):
        return 1
    
    # Otherwise, return 2
    return 2

# Read input
n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

# Output the result
print(min_rows_for_mirroring(n, m, a))