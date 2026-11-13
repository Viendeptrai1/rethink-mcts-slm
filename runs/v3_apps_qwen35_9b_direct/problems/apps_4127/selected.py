import sys

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    A_str, B_str = input_data.split()
    A = int(A_str)
    B = float(B_str)
    result = int(A * B)
    print(result)

if __name__ == "__main__":
    solve()