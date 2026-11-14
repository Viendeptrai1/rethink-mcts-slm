import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    
    for C in range(1, 4):
        if (A * B * C) % 2 == 1:
            print("Yes")
            return
    print("No")

if __name__ == "__main__":
    solve()