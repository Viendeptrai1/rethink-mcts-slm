def max_tandem_repeat_length(s, k):
    n = len(s)
    max_l = 0

    # Check for all possible tandem repeats
    for i in range(n):
        for j in range(i + 1, n):
            # Check if s[i:j] is a tandem repeat
            repeat_length = j - i
            if repeat_length % 2 == 0:
                half_length = repeat_length // 2
                if s[i:i + half_length] == s[j:j + half_length]:
                    max_l = max(max_l, repeat_length + k)

    return max_l

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    k = int(data[1])
    print(max_tandem_repeat_length(s, k))