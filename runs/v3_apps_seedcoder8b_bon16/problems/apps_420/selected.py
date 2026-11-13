def min_rows_matrix_b(a):
    n, m = len(a), len(a[0])
    
    def is_mirrorable(rows):
        b = a[:rows]
        c = b + b[::-1]
        return c[:n] == a
    
    for i in range(1, n + 1):
        if is_mirrorable(i):
            return i
    
    return n

# Read input
n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

# Calculate and print the result
print(min_rows_matrix_b(a))