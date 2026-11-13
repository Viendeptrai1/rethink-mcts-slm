import sys

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    parts = input_data.split()
    A = parts[0]
    B = parts[1]
    C = parts[2]
    
    if A[-1] == B[0] and B[-1] == C[0]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()