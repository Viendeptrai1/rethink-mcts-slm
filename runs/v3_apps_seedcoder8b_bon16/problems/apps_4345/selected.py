def can_split_sequence(n, a):
    if n <= 1:
        print("YES")
        print("0" * n)
        return

    # Identify potential start of the increasing sequence
    inc = [0] * n
    inc[0] = 1  # The first element can always be part of increasing

    for i in range(1, n):
        if a[i] > a[i - 1]:
            inc[i] = 1

    # Identify potential end of the decreasing sequence
    dec = [0] * n
    dec[-1] = 1  # The last element can always be part of decreasing

    for i in range(n - 2, -1, -1):
        if a[i] > a[i + 1]:
            dec[i] = 1

    # Validate the possibility of splitting
    for i in range(n):
        if (inc[i] == 1 and dec[i] == 1):
            print("NO")
            return

    # If we can split, prepare result
    res = [0] * n
    for i in range(n):
        if inc[i] == 1:
            res[i] = 0
        else:
            res[i] = 1

    print("YES")
    print(" ".join(map(str, res)))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    a = list(map(int, data[1:]))

    can_split_sequence(n, a)

if __name__ == "__main__":
    main()