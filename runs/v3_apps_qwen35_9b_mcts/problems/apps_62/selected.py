import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # Memoization cache: key is tuple of sorted a, value is True if current player wins
    memo = {}

    def get_winner(state):
        # state is a sorted tuple of integers
        if state in memo:
            return memo[state]

        # Check if any move is possible
        # Move 1: Reduce one pile by x (1 <= x <= pile)
        # Move 2: Reduce all piles by x (1 <= x <= min(piles))
        
        # If no moves possible (all zeros), current player loses
        if all(x == 0 for x in state):
            memo[state] = False
            return False

        # Check Move 2: Global reduction
        # Can reduce all by x where 1 <= x <= min(state)
        min_val = state[0]
        if min_val > 0:
            # Try all possible global moves
            for x in range(1, min_val + 1):
                new_state = tuple(sorted([y - x for y in state]))
                if not get_winner(new_state):
                    memo[state] = True
                    return True

        # Check Move 1: Single pile reduction
        # Try reducing each pile by x from 1 to pile value
        for i in range(n):
            val = state[i]
            if val > 0:
                for x in range(1, val + 1):
                    new_state_list = list(state)
                    new_state_list[i] -= x
                    new_state = tuple(sorted(new_state_list))
                    if not get_winner(new_state):
                        memo[state] = True
                        return True

        # If no winning move found
        memo[state] = False
        return False

    # Initial state must be sorted for consistent memoization keys
    initial_state = tuple(sorted(a))
    
    if get_winner(initial_state):
        print("BitLGM")
    else:
        print("BitAryo")

if __name__ == "__main__":
    solve()