import sys

def thanos_sort_max_length(n, arr):
    def is_sorted(subarr):
        return all(subarr[i] <= subarr[i + 1] for i in range(len(subarr) - 1))
    
    def max_sorted_length(arr):
        if len(arr) == 1:
            return 1
        mid = len(arr) // 2
        left_sorted_len = max_sorted_length(arr[:mid])
        right_sorted_len = max_sorted_length(arr[mid:])
        combined_sorted_len = 0
        if is_sorted(arr[:mid]) and is_sorted(arr[mid:]):
            i, j = 0, mid
            while i < mid and j < len(arr):
                if arr[i] <= arr[j]:
                    combined_sorted_len += 1
                    i += 1
                else:
                    j += 1
        return max(left_sorted_len, right_sorted_len, combined_sorted_len)
    
    return max_sorted_length(arr)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    print(thanos_sort_max_length(n, arr))

if __name__ == "__main__":
    main()