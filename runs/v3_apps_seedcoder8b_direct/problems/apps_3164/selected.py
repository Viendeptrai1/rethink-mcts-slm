def longest_consecutive_subarray_twice(arr):
    from collections import defaultdict

    n = len(arr)
    max_length = 0
    left = 0
    count = defaultdict(int)
    unique_count = 0

    for right in range(n):
        count[arr[right]] += 1
        if count[arr[right]] == 1:
            unique_count += 1
        elif count[arr[right]] == 2:
            unique_count += 1
        elif count[arr[right]] == 3:
            unique_count -= 1

        while unique_count < right - left + 1:
            count[arr[left]] -= 1
            if count[arr[left]] == 0:
                unique_count -= 1
            elif count[arr[left]] == 1:
                unique_count -= 1
            left += 1

        if unique_count == right - left + 1:
            max_length = max(max_length, right - left + 1)

    return max_length

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    arr = list(map(int, data[1:]))
    
    result = longest_consecutive_subarray_twice(arr)
    print(result)