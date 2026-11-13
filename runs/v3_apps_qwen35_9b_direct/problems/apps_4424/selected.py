import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    K = int(input_data[0])
    X = int(input_data[1])
    total = K * 500
    if total >= X:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()