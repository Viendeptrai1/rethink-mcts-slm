def find_minimum_i(n, k, A0):
    def p(x):
        y = [0] * (len(x) + 1)
        for i in range(1, len(x) + 1):
            y[i] = y[i - 1] + x[i - 1]
        return y

    A = A0[:]
    i = 0
    while True:
        if any(a >= k for a in A):
            return i
        A = p([a - 1 for a in A])
        i += 1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    A0 = list(map(int, data[2:2 + n]))
    
    result = find_minimum_i(n, k, A0)
    print(result)