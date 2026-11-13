import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    C = int(input_data[2])
    
    space_in_bottle1 = A - B
    transfer_amount = min(space_in_bottle1, C)
    remaining_in_bottle2 = C - transfer_amount
    
    print(remaining_in_bottle2)

if __name__ == "__main__":
    solve()