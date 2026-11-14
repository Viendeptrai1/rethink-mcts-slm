import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    candidates = [A + B, A - B, A * B]
    print(max(candidates))

if __name__ == "__main__":
    solve()