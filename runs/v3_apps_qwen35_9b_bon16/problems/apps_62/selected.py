import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    idx = 1
    for _ in range(n):
        a.append(int(input_data[idx]))
        idx += 1
    
    # Memoization cache
    memo = {}
    
    def can_win(state_tuple):
        if state_tuple in memo:
            return memo[state_tuple]
        
        # Convert tuple back to list for processing if needed, but we work with tuple
        # Check if any move is possible
        # A move is possible if at least one a_i > 0
        
        current_list = list(state_tuple)
        max_val = 0
        for x in current_list:
            if x > max_val:
                max_val = x
        
        if max_val == 0:
            # No moves possible, current player loses
            memo[state_tuple] = False
            return False
        
        # Player can choose one index i and reduce a[i] by x (1 <= x <= a[i])
        # This is equivalent to changing a[i] to any value y such that 0 <= y < a[i]
        moves = []
        
        # Option 1: Single pile move
        for i in range(n):
            if current_list[i] > 0:
                # Can change a[i] to any value from 0 to a[i]-1
                for new_val in range(current_list[i]):
                    new_state = list(state_tuple)
                    new_state[i] = new_val
                    moves.append(tuple(new_state))
        
        # Option 2: All piles move
        # Choose x (1 <= x <= min(a_i))
        min_val = current_list[0]
        for i in range(1, n):
            if current_list[i] < min_val:
                min_val = current_list[i]
        
        if min_val > 0:
            for x in range(1, min_val + 1):
                new_state = tuple(val - x for val in state_tuple)
                moves.append(new_state)
        
        # If there exists a move to a losing state, then current state is winning
        for next_state in moves:
            if not can_win(next_state):
                memo[state_tuple] = True
                return True
        
        # All moves lead to winning states for the opponent
        memo[state_tuple] = False
        return False

    initial_state = tuple(a)
    if can_win(initial_state):
        print("BitLGM")
    else:
        print("BitAryo")

if __name__ == "__main__":
    solve()