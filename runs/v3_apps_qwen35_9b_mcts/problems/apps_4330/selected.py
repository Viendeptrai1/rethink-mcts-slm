import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    
    if (A + B) % 2 == 0:
        K = (A + B) // 2
        print(K)
    else:
        print("IMPOSSIBLE")

if __name__ == "__main__":
    solve()