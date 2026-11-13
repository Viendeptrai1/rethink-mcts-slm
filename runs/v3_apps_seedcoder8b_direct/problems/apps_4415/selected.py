def find_sequences(n, a):
    from collections import deque

    # Sort the array to help identify the increasing and decreasing sequences
    a.sort()

    # Initialize two deques to store the increasing and decreasing sequences
    increasing = deque()
    decreasing = deque()

    # Use two pointers to traverse the sorted array
    left, right = 0, n - 1

    # Alternate between adding elements to the increasing and decreasing sequences
    while left <= right:
        if len(increasing) == 0 or a[left] > increasing[-1]:
            increasing.append(a[left])
            left += 1
        elif len(decreasing) == 0 or a[right] < decreasing[-1]:
            decreasing.append(a[right])
            right -= 1
        else:
            # If neither condition is met, it's impossible to split the array
            print("NO")
            return

    # Print the result
    print("YES")
    print(len(increasing))
    print(" ".join(map(str, increasing)))
    print(len(decreasing))
    print(" ".join(map(str, decreasing)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

find_sequences(n, a)