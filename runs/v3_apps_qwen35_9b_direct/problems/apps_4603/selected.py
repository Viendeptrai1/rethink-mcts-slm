import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    C = int(input_data[2])
    D = int(input_data[3])
    
    train_min = min(A, B)
    bus_min = min(C, D)
    
    print(train_min + bus_min)

if __name__ == "__main__":
    solve()