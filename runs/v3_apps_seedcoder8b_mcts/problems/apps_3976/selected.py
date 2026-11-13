def find_valid_qs(n, m, p, a, b):
    from collections import Counter

    b_count = Counter(b)
    valid_qs = []

    for q in range(1, n - m * p + 2):
        a_window = a[q-1:q-1+m*p:p]
        a_count = Counter(a_window)
        if a_count == b_count:
            valid_qs.append(q)

    print(len(valid_qs))
    if valid_qs:
        print(" ".join(map(str, valid_qs)))

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    p = int(data[2])
    a = list(map(int, data[3:3+n]))
    b = list(map(int, data[3+n:3+n+m]))
    
    find_valid_qs(n, m, p, a, b)