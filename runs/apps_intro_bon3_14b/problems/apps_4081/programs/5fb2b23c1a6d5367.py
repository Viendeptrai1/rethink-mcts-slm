import sys

def main():
    import sys
    import bisect
    
    def read_ints():
        return list(map(int, sys.stdin.read().split()))
    
    data = read_ints()
    n = data[0]
    a = data[1:]
    
    # Initialize the DP table
    dp = [0] * (n + 1)
    path = [''] * (n + 1)
    
    # Arrays to store the indices of the smallest and largest elements
    smallest = [0] * (n + 1)
    largest = [0] * (n + 1)
    
    # Fill the smallest array
    smallest[0] = -1
    for i in range(n):
        j = bisect.bisect_left(smallest, a[i])
        if j == len(smallest):
            smallest.append(a[i])
        else:
            smallest[j] = a[i]
        if j > dp[a[i]]:
            dp[a[i]] = j
            path[a[i]] = path[smallest[j-1]] + 'L'
    
    # Fill the largest array
    largest[n] = n + 1
    for i in range(n-1, -1, -1):
        j = bisect.bisect_right(largest, a[i])
        if j == 0:
            largest.insert(0, a[i])
        else:
            largest[j-1] = a[i]
        if n - i + 1 > dp[a[i]]:
            dp[a[i]] = n - i + 1
            path[a[i]] = path[largest[j]] + 'R'
    
    # Find the maximum length of the increasing sequence
    max_length = max(dp)
    result_path = path[dp.index(max_length)]
    
    # Print the result
    print(max_length)
    print(result_path)

if __name__ == "__main__":
    main()