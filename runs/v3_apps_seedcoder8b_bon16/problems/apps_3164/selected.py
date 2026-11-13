def find_longest_subarray_with_pairs(arr):
    from collections import defaultdict

    count_map = defaultdict(int)
    left = 0
    max_length = 0

    for right in range(len(arr)):
        count_map[arr[right]] += 1

        # While the number of occurrences of the current element is greater than 2, shrink the window
        while count_map[arr[right]] > 2:
            count_map[arr[left]] -= 1
            left += 1

        # Check if the window contains elements that appear exactly twice
        current_length = right - left + 1
        if all(count == 2 for key, count in count_map.items() if key in arr[left:right + 1]):
            max_length = max(max_length, current_length)

    return max_length

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    arr = list(map(int, data[1:N + 1]))

    print(find_longest_subarray_with_pairs(arr))

if __name__ == "__main__":
    main()