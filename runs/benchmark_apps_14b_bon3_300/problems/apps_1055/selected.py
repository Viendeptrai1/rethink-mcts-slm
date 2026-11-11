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
        for i in range(mid):
            if is_sorted(arr[i:i + left_sorted_len]) and is_sorted(arr[mid:mid + right_sorted_len]):
                combined_sorted_len = max(combined_sorted_len, left_sorted_len + right_sorted_len)
                break
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