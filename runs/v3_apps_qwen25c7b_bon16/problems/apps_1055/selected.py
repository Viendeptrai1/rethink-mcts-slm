import sys
from typing import List

def thanos_sort_max_length(arr: List[int]) -> int:
    def is_sorted(sub_arr: List[int]) -> bool:
        return all(sub_arr[i] <= sub_arr[i + 1] for i in range(len(sub_arr) - 1))

    def max_length_recursive(left: int, right: int) -> int:
        if left > right:
            return 0
        if is_sorted(arr[left:right + 1]):
            return right - left + 1
        mid = (left + right) // 2
        return max(max_length_recursive(left, mid), max_length_recursive(mid + 1, right))

    return max_length_recursive(0, len(arr) - 1)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    print(thanos_sort_max_length(arr))