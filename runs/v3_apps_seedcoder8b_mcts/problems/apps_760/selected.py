def max_tandem_repeat_length(s, k):
    n = len(s)
    max_length = 0

    for i in range(n):
        for j in range(i + 1, n + 1):
            repeat_length = 2 * (j - i)
            if repeat_length <= n + k:
                max_length = max(max_length, repeat_length)

    return max_length

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    k = int(data[1])
    print(max_tandem_repeat_length(s, k))