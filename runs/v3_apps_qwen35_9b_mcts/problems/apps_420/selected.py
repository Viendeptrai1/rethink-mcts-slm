import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    matrix = []
    for _ in range(n):
        row = []
        for _ in range(m):
            row.append(int(next(iterator)))
        matrix.append(row)

    current_n = n
    while current_n % 2 == 0:
        half = current_n // 2
        is_mirror = True
        for i in range(half):
            if matrix[i] != matrix[current_n - 1 - i]:
                is_mirror = False
                break
        if is_mirror:
            current_n = half
        else:
            break

    print(current_n)

if __name__ == "__main__":
    solve()