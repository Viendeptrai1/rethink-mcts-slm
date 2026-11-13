def min_rows_for_symmetric_mirroring(n, m, a):
    def is_symmetric(start_row):
        for i in range(start_row, n):
            if a[i] != a[2 * start_row - i - 1]:
                return False
        return True

    for x in range(1, n + 1):
        if is_symmetric(x):
            return x

    return n

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = []
    index = 2
    for _ in range(n):
        a.append(list(map(int, data[index:index + m])))
        index += m
    
    result = min_rows_for_symmetric_mirroring(n, m, a)
    print(result)