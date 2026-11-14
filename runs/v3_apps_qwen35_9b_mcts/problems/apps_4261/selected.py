import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    C = int(input_data[2])
    
    remaining_capacity = A - B
    transfer_amount = min(C, remaining_capacity)
    result = C - transfer_amount
    
    print(result)

if __name__ == "__main__":
    solve()