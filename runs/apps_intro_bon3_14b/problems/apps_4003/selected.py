import sys

def solve():
    import sys
    import bisect

    def main():
        import sys
        import bisect

        n = int(sys.stdin.readline().strip())
        a = list(map(int, sys.stdin.readline().strip().split()))

        # Initialize the DP table and the path table
        dp = [0] * n
        path = [-1] * n
        dp[0] = 1
        path[0] = 0

        # Use a list to keep track of the smallest ending value of increasing subsequences of different lengths
        lis = [a[0]]

        for i in range(1, n):
            if a[i] > lis[-1]:
                # If a[i] is greater than the last element of lis, extend the lis
                lis.append(a[i])
                dp[i] = len(lis)
                path[i] = path[i - 1]
            else:
                # Find the position to replace in lis
                pos = bisect.bisect_left(lis, a[i])
                lis[pos] = a[i]
                dp[i] = pos + 1
                if pos == 0:
                    path[i] = i
                else:
                    path[i] = path[i - 1]

        # The length of the longest increasing subsequence
        k = max(dp)

        # Reconstruct the path
        result = []
        current = dp.index(k)
        while current != -1:
            if current == 0 or a[current] > a[current - 1]:
                result.append('L')
            else:
                result.append('R')
            current = path[current]

        # Reverse the result to get the correct order
        result.reverse()

        # Print the result
        print(k)
        print(''.join(result))

    if __name__ == "__main__":
        main()

solve()