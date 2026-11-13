def thanos_sort_max_length(n, arr):
    def is_sorted(subarr):
        return all(subarr[i] <= subarr[i + 1] for i in range(len(subarr) - 1))

    def max_sorted_length(start, end):
        if start == end:
            return 1
        if is_sorted(arr[start:end + 1]):
            return end - start + 1

        mid = (start + end) // 2
        left_length = max_sorted_length(start, mid)
        right_length = max_sorted_length(mid + 1, end)

        return max(left_length, right_length)

    return max_sorted_length(0, n - 1)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    arr = list(map(int, data[1:n+1]))
    
    result = thanos_sort_max_length(n, arr)
    print(result)