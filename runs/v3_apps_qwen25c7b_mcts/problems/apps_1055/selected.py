def thanos_sort(arr):
    def is_sorted(subarr):
        return all(subarr[i] <= subarr[i + 1] for i in range(len(subarr) - 1))

    def dfs(subarr):
        if is_sorted(subarr):
            return len(subarr)
        mid = len(subarr) // 2
        left_len = dfs(subarr[:mid])
        right_len = dfs(subarr[mid:])
        return max(left_len, right_len)

    return dfs(arr)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
arr = list(map(int, data[1:]))

print(thanos_sort(arr))