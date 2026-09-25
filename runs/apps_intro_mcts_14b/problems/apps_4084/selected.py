import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = int(data[1])
    B = int(data[2])
    
    # Calculate the length of one full cycle
    cycle_length = A + B
    
    # Determine how many full cycles fit into N
    full_cycles = N // cycle_length
    
    # Calculate the number of blue balls in full cycles
    blue_balls_in_full_cycles = full_cycles * A
    
    # Calculate the remaining balls after full cycles
    remaining_balls = N % cycle_length
    
    # Calculate the number of blue balls in the remaining part
    blue_balls_in_remaining = min(remaining_balls, A)
    
    # Total number of blue balls
    total_blue_balls = blue_balls_in_full_cycles + blue_balls_in_remaining
    
    print(total_blue_balls)

if __name__ == "__main__":
    main()