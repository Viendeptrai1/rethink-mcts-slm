import sys

def main():
    import sys
    import bisect

    def read_ints():
        return list(map(int, sys.stdin.read().split()))

    n = read_ints()[0]
    a = read_ints()[1:]

    # Initialize the DP table
    dp = [0] * n
    dp[0] = a[0]
    pos = [0] * n
    pos[0] = 0

    for i in range(1, n):
        if a[i] > dp[-1]:
            dp.append(a[i])
            pos[len(dp) - 1] = i
        else:
            idx = bisect.bisect_left(dp, a[i])
            dp[idx] = a[i]
            pos[idx] = i

    k = len(dp)
    result = [''] * k
    current_pos = pos[k - 1]

    for i in range(k - 1, -1, -1):
        if current_pos == 0:
            result[i] = 'L'
        elif current_pos == n - 1:
            result[i] = 'R'
        else:
            if dp[i] == a[current_pos]:
                result[i] = 'L'
                current_pos -= 1
            else:
                result[i] = 'R'
                current_pos += 1

    print(k)
    print(''.join(result))

if __name__ == "__main__":
    main()