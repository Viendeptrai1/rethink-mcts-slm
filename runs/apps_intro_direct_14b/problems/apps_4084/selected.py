import sys

def count_blue_balls(N, A, B):
    if A == 0:
        return 0
    cycle_length = A + B
    full_cycles = N // cycle_length
    remaining_balls = N % cycle_length
    blue_in_full_cycles = full_cycles * A
    blue_in_remaining = min(remaining_balls, A)
    return blue_in_full_cycles + blue_in_remaining

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = int(data[1])
    B = int(data[2])
    result = count_blue_balls(N, A, B)
    print(result)

if __name__ == "__main__":
    main()