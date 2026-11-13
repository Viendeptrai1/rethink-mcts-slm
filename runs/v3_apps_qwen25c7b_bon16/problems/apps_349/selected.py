def can_make_increasing(n, m, a, b):
    def is_strictly_increasing(seq):
        return all(x < y for x, y in zip(seq, seq[1:]))

    a_rows = [a[i] for i in range(n)]
    b_rows = [b[i] for i in range(n)]
    a_cols = [list(a[j][i] for j in range(n)) for i in range(m)]
    b_cols = [list(b[j][i] for j in range(n)) for i in range(m)]

    a_not_increasing_rows = [i for i, row in enumerate(a_rows) if not is_strictly_increasing(row)]
    b_not_increasing_rows = [i for i, row in enumerate(b_rows) if not is_strictly_increasing(row)]
    a_not_increasing_cols = [i for i, col in enumerate(a_cols) if not is_strictly_increasing(col)]
    b_not_increasing_cols = [i for i, col in enumerate(b_cols) if not is_strictly_increasing(col)]

    return len(set(a_not_increasing_rows + b_not_increasing_rows)) == 0 and \
           len(set(a_not_increasing_cols + b_not_increasing_cols)) == 0

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

a = []
for i in range(n):
    a.append([int(data[2 + i * m + j]) for j in range(m)])

b = []
for i in range(n):
    b.append([int(data[2 + n * m + i * m + j]) for j in range(m)])

# Output result
if can_make_increasing(n, m, a, b):
    print("Possible")
else:
    print("Impossible")