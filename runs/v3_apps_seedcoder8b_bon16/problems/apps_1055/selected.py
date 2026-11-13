def thanos_sort_max_length(n, array):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def thanos_sort(arr):
        if len(arr) <= 1 or is_sorted(arr):
            return len(arr)

        half = len(arr) // 2
        # Check both halves and return the maximum length of sorted array that can be obtained
        return max(thanos_sort(arr[:half]), thanos_sort(arr[half:]))

    return thanos_sort(array)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    array = list(map(int, data[1:]))
    
    print(thanos_sort_max_length(n, array))