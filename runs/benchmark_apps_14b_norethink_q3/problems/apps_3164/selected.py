import sys

def longest_subarray_with_each_element_twice(arr):
    n = len(arr)
    if n < 2:
        return 0

    count_map = {}
    left = 0
    max_length = 0

    for right in range(n):
        if arr[right] in count_map:
            count_map[arr[right]] += 1
        else:
            count_map[arr[right]] = 1

        while count_map[arr[right]] > 2:
            count_map[arr[left]] -= 1
            if count_map[arr[left]] == 0:
                del count_map[arr[left]]
            left += 1

        if all(count == 2 for count in count_map.values()):
            max_length = max(max_length, right - left + 1)

    return max_length

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    print(longest_subarray_with_each_element_twice(arr))