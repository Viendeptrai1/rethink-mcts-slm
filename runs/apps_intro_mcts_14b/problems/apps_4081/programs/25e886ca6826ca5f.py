import sys

def main():
    import sys
    import bisect

    def read_input():
        import sys
        return sys.stdin.read().split()

    data = read_input()
    n = int(data[0])
    a = list(map(int, data[1:]))

    # Initialize variables
    left = 0
    right = n - 1
    lis = []
    moves = []

    while left <= right:
        if a[left] < a[right]:
            if not lis or a[left] > lis[-1]:
                lis.append(a[left])
                moves.append('L')
                left += 1
            else:
                if a[right] > lis[-1]:
                    lis.append(a[right])
                    moves.append('R')
                    right -= 1
                else:
                    left += 1
        else:
            if not lis or a[right] > lis[-1]:
                lis.append(a[right])
                moves.append('R')
                right -= 1
            else:
                if a[left] > lis[-1]:
                    lis.append(a[left])
                    moves.append('L')
                    left += 1
                else:
                    right -= 1

    # Output the result
    print(len(lis))
    print(''.join(moves))

if __name__ == "__main__":
    main()