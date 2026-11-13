import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    
    # The condition |A - K| = |B - K| implies K is the midpoint of A and B.
    # K = (A + B) / 2
    # For K to be an integer, (A + B) must be even.
    if (A + B) % 2 == 0:
        K = (A + B) // 2
        print(K)
    else:
        print("IMPOSSIBLE")

if __name__ == "__main__":
    solve()