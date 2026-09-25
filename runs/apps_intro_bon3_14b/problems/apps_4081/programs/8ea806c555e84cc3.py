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
    path = ['L'] * n
    pos = [0] * n
    pos[0] = 0

    for i in range(1, n):
        if a[i] > dp[-1]:
            dp.append(a[i])
            path[len(dp) - 1] = 'R'
            pos[len(dp) - 1] = i
        else:
            idx = bisect.bisect_left(dp, a[i])
            dp[idx] = a[i]
            path[idx] = 'R' if i == n - 1 else 'L'
            pos[idx] = i

    k = len(dp)
    result_path = []
    current_pos = pos[k - 1]

    for i in range(k - 1, -1, -1):
        if path[i] == 'L':
            result_path.append('L')
            current_pos -= 1
        else:
            result_path.append('R')
            current_pos += 1

    result_path.reverse()

    print(k)
    print(''.join(result_path))

if __name__ == "__main__":
    main()