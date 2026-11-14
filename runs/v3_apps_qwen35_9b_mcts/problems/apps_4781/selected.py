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

    current_player = K - 1  # Convert to 0-based index
    total_time = 0
    explosion_time = 3 * 60 + 30  # 3 minutes 30 seconds = 210 seconds

    for _ in range(N):
        try:
            T_str = next(iterator)
            Z = next(iterator)
            T = int(T_str)
        except StopIteration:
            break

        total_time += T

        if total_time > explosion_time:
            # The box explodes during this player's turn
            print(current_player + 1)
            return

        if Z == 'T':
            # Pass to the left (next player in circle)
            current_player = (current_player + 1) % 8
        # If 'N' or 'P', the box stays with the current player

if __name__ == "__main__":
    solve()