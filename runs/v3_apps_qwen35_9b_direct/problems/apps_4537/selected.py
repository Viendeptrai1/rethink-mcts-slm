import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    result = max(A + B, A - B, A * B)
    print(result)

if __name__ == "__main__":
    solve()