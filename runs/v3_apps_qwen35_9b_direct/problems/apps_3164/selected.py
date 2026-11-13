import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    if n == 0:
        print(0)
        return

    arr = [int(x) for x in input_data[1:]]

    # Dictionary to store the count of each number in the current window
    count = {}
    left = 0
    max_len = 0

    for right in range(n):
        num = arr[right]
        count[num] = count.get(num, 0) + 1

        # If count exceeds 2, shrink window from left until count is <= 2
        while count[num] > 2:
            left_num = arr[left]
            count[left_num] -= 1
            if count[left_num] == 0:
                del count[left_num]
            left += 1

        # Update max length
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len

    print(max_len)

if __name__ == "__main__":
    solve()