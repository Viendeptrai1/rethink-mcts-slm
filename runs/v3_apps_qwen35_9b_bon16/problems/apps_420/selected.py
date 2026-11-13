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

    # We start from the full matrix and try to "unmirror" as much as possible
    # The condition to unmirror is that the bottom half must be the exact mirror of the top half.
    # If it is, we can reduce the problem to the top half.
    # We repeat this until the condition fails.
    
    curr_n = n
    while curr_n % 2 == 0:
        half = curr_n // 2
        # Check if the bottom half is the mirror of the top half
        is_symmetric = True
        for i in range(half):
            # Row i should match row (curr_n - 1 - i)
            for j in range(m):
                if matrix[i][j] != matrix[curr_n - 1 - i][j]:
                    is_symmetric = False
                    break
            if not is_symmetric:
                break
        
        if is_symmetric:
            curr_n = half
        else:
            break
            
    print(curr_n)

if __name__ == '__main__':
    solve()