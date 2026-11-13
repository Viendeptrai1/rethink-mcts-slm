import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])

    # We need to find if there exists C in {1, 2, 3} such that A * B * C is odd.
    # A product is odd if and only if all factors are odd.
    # So we need A, B, and C to all be odd.
    # Since we can choose C, we just need to check if there is an odd number in {1, 2, 3}.
    # The odd numbers in {1, 2, 3} are 1 and 3.
    # Therefore, if A is odd and B is odd, we can pick C = 1 (or 3) and the product will be odd.
    # If either A or B is even, then no matter what C we pick, the product will be even.

    if A % 2 == 1 and B % 2 == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()