def find_initial_sequences(n, a):
    if n == 0:
        print("YES")
        print("")
        return

    # Initialize pointers and result array
    inc = [0] * n
    dec = [0] * n
    inc[0] = 1  # First element is part of the increasing sequence

    # Traverse the array to determine the increasing sequence
    for i in range(1, n):
        if a[i] > a[i - 1]:
            inc[i] = 1
        else:
            break

    # If the entire array is increasing, we can return
    if inc[-1] == 1:
        print("YES")
        print(" ".join(map(str, inc)))
        return

    # Traverse the array to determine the decreasing sequence
    for i in range(n - 1, -1, -1):
        if i == n - 1 or a[i] > a[i + 1]:
            dec[i] = 1
        else:
            break

    # If the entire array is decreasing, we can return
    if dec[0] == 1:
        print("YES")
        print(" ".join(map(str, dec)))
        return

    # Check if there's a valid split
    for i in range(n - 1):
        if inc[i] == 1 and dec[i + 1] == 1:
            # Check if the increasing sequence is strictly increasing
            # and the decreasing sequence is strictly decreasing
            if all(a[j] < a[j + 1] for j in range(i) if inc[j] == 1) and \
               all(a[j] > a[j + 1] for j in range(i + 1, n) if dec[j] == 1):
                print("YES")
                print(" ".join(map(str, inc)))
                return

    print("NO")

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Call the function with the input data
find_initial_sequences(n, a)