def thanos_sort_max_length(n, arr):
    def is_sorted(subarray):
        return all(subarray[i] <= subarray[i + 1] for i in range(len(subarray) - 1))

    def max_sorted_length(start, end):
        if start >= end:
            return 0
        if is_sorted(arr[start:end]):
            return end - start
        mid = (start + end) // 2
        return max(max_sorted_length(start, mid), max_sorted_length(mid, end))

    return max_sorted_length(0, n)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    arr = list(map(int, data[1:n+1]))
    print(thanos_sort_max_length(n, arr))