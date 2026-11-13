import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    T = int(input_data[0])
    X = int(input_data[1])
    result = T / X
    print(f"{result:.10f}")

if __name__ == "__main__":
    solve()