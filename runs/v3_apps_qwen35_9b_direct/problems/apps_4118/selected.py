import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    
    if 1 <= A <= 9 and 1 <= B <= 9:
        print(A * B)
    else:
        print(-1)

if __name__ == "__main__":
    solve()