def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:n+2]))

    def p(x):
        m = len(x)
        y = [0] * (m + 1)
        for i in range(m):
            y[i + 1] = y[i] + x[i]
        return y

    i = 0
    while True:
        if any(value >= k for value in A):
            print(i)
            return
        A = p([a - 1 for a in A])
        i += 1

if __name__ == "__main__":
    main()