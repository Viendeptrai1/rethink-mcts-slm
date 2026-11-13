import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        K = int(next(iterator))
        N = int(next(iterator))
    except StopIteration:
        return

    total_time = 0
    current_player = K
    
    # The box explodes after 3 minutes and 30 seconds = 210 seconds
    explosion_time = 210
    
    for _ in range(N):
        try:
            T_str = next(iterator)
            Z = next(iterator)
            T = int(T_str)
        except StopIteration:
            break
        
        total_time += T
        
        # Check if the box explodes during this question's time window
        # The problem states: "The box will surely explode on a player's turn."
        # This implies we check if the cumulative time reaches or exceeds 210.
        if total_time >= explosion_time:
            print(current_player)
            return
        
        # Determine next state based on answer
        if Z == 'T':
            # Pass to the first player seated on his left
            # Players are 1-8 in a circle. Left usually means (current + 1) % 8, but adjusted for 1-based indexing.
            # If current is 8, next is 1. Otherwise current + 1.
            current_player = current_player % 8 + 1
        else:
            # Incorrect or skipped: immediately given the next question (same player)
            # current_player remains the same

if __name__ == "__main__":
    solve()