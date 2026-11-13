import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])

    # For the product A * B * C to be odd, all three numbers must be odd.
    # We need to check if there exists an odd integer C in [1, 3].
    # The odd integers in [1, 3] are 1 and 3.
    # So we just need to check if A is odd AND B is odd.
    # If both are odd, we can pick C = 1 (or 3) and the product will be odd.
    # If either A or B is even, no matter what C we pick, the product will be even.

    if A % 2 == 1 and B % 2 == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()