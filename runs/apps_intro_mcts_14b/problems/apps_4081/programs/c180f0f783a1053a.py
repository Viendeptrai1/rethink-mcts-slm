import sys

def main():
    import sys
    import bisect

    def read_input():
        input = sys.stdin.read
        data = input().split()
        return data

    data = read_input()
    n = int(data[0])
    a = list(map(int, data[1:]))

    # Create a list of tuples (value, index)
    indexed_a = [(a[i], i) for i in range(n)]
    # Sort by value
    indexed_a.sort()

    # Initialize the DP table
    dp = [0] * n
    # Initialize the parent table to reconstruct the path
    parent = [-1] * n
    # Initialize the position table to keep track of the last occurrence of each value
    pos = [-1] * n

    max_length = 0
    max_index = -1

    for i in range(n):
        value, index = indexed_a[i]
        # Find the position to insert the current value in the dp array
        j = bisect.bisect_left(dp, value)
        if j < max_length:
            parent[index] = pos[dp[j-1]]
        dp[j] = value
        pos[value-1] = index
        if j >= max_length:
            max_length = j + 1
            max_index = index

    # Reconstruct the path
    result = []
    current = max_index
    while current != -1:
        if indexed_a[current][1] == 0:
            result.append('L')
        else:
            result.append('R')
        current = parent[current]

    result.reverse()

    # Print the result
    print(max_length)
    print(''.join(result))

if __name__ == "__main__":
    main()