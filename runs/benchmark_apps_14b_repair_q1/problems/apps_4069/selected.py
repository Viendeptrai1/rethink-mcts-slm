import sys

def main():
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    X, K, D = readints()
    
    # Calculate the number of full steps we can take towards zero
    full_steps = K // 2
    
    # Calculate the remaining steps after taking full_steps
    remaining_steps = K % 2
    
    # Calculate the position after taking full_steps towards zero
    position_after_full_steps = X - full_steps * D
    
    # If there is a remaining step, adjust the position
    if remaining_steps == 1:
        position_after_full_steps += D
    
    # Calculate the absolute value of the final position
    final_position = abs(position_after_full_steps)
    
    # Calculate the absolute value of the position if we had taken one more step in the opposite direction
    alternative_position = abs(position_after_full_steps - D)
    
    # The minimum possible absolute value is the smaller of the two
    result = min(final_position, alternative_position)
    
    print(result)

if __name__ == "__main__":
    main()