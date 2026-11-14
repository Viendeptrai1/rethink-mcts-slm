import sys
from collections import defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    arr = []
    for _ in range(n):
        arr.append(int(next(iterator)))

    freq = defaultdict(int)
    left = 0
    max_len = 0

    for right in range(n):
        val = arr[right]
        freq[val] += 1

        while freq[val] > 2:
            left_val = arr[left]
            freq[left_val] -= 1
            left += 1

        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len

    print(max_len)

if __name__ == "__main__":
    solve()