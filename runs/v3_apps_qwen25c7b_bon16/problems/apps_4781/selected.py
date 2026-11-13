# Import necessary library
import sys

def find_exploding_player(K, N, questions):
    # Define the initial position of the box
    current_position = K - 1
    
    # Process each question
    for _, answer in questions:
        if answer == 'N' or answer == 'P':
            continue
        
        # Move to the next player
        current_position = (current_position + 1) % 8
    
    # Return the player who had the box when it exploded
    return current_position + 1

# Read input from standard input
if __name__ == "__main__":
    K = int(sys.stdin.readline().strip())
    N = int(sys.stdin.readline().strip())
    questions = [tuple(map(str, sys.stdin.readline().strip().split())) for _ in range(N)]
    
    # Convert times to integers (not needed for this problem)
    questions = [(int(t), z) for t, z in questions]
    
    # Find and print the exploding player
    result = find_exploding_player(K, N, questions)
    print(result)