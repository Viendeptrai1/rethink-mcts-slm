def thanos_sort_max_length(n, arr):
    def is_sorted(subarr):
        return all(subarr[i] <= subarr[i + 1] for i in range(len(subarr) - 1))

    def max_length_recursive(start, end):
        if start >= end:
            return 0
        mid = (start + end) // 2
        left_length = max_length_recursive(start, mid)
        right_length = max_length_recursive(mid + 1, end)
        if is_sorted(arr[start:mid + 1]) and is_sorted(arr[mid + 1:end + 1]):
            return max(left_length, right_length)
        elif is_sorted(arr[start:mid + 1]):
            return left_length + max_length_recursive(mid + 1, end)
        elif is_sorted(arr[mid + 1:end + 1]):
            return right_length + max_length_recursive(start, mid)
        else:
            return max(max_length_recursive(start, mid), max_length_recursive(mid + 1, end))

    return max_length_recursive(0, n - 1)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
arr = list(map(int, data[1:]))

print(thanos_sort_max_length(n, arr))