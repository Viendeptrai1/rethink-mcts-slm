import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]

    # For gear i (0-indexed):
    # Initial value: a[i]
    # Target value: i
    # Rotation direction: clockwise if i is even, counter-clockwise if i is odd.
    # Clockwise: value increases (0 -> 1 -> ... -> n-1 -> 0)
    # Counter-clockwise: value decreases (0 -> n-1 -> ... -> 1 -> 0)
    #
    # Let k be the number of button presses.
    # For even i: (a[i] + k) % n = i  => k = (i - a[i]) % n
    # For odd i:  (a[i] - k) % n = i  => k = (a[i] - i) % n

    k = -1
    possible = True

    for i in range(n):
        if i % 2 == 0:
            # Even index: clockwise rotation
            # We need (a[i] + k) % n == i
            # k = (i - a[i]) % n
            req_k = (i - a[i]) % n
        else:
            # Odd index: counter-clockwise rotation
            # We need (a[i] - k) % n == i
            # -k = (i - a[i]) % n
            # k = (a[i] - i) % n
            req_k = (a[i] - i) % n

        if k == -1:
            k = req_k
        elif k != req_k:
            possible = False
            break

    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()