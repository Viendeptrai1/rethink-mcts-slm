import sys

def solve():
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return
        n = int(input_data)
    except ValueError:
        return

    height = 0
    cubes_used = 0
    level_cubes = 0

    while True:
        # Calculate cubes needed for the next level
        # Level i (1-indexed) needs 1 + 2 + ... + i cubes
        # But we are building level by level.
        # Let's track:
        # current_level = 1, 2, 3...
        # cubes_in_current_level = 1, 3, 6...
        # total_cubes_needed = sum of cubes_in_current_level for all levels built so far.

        # Actually, let's re-simulate based on the problem description:
        # Level 1: 1 cube
        # Level 2: 1+2 = 3 cubes
        # Level 3: 1+2+3 = 6 cubes
        # ...
        # Level i: i*(i+1)//2 cubes
        
        # We need to check if we have enough cubes to add the next level.
        
        # Current height is 'height'. We want to try adding level 'height + 1'.
        # Cubes needed for level 'height + 1' is (height + 1) * (height + 2) // 2.
        
        next_level = height + 1
        cubes_for_next_level = next_level * (next_level + 1) // 2
        
        if cubes_used + cubes_for_next_level <= n:
            cubes_used += cubes_for_next_level
            height = next_level
        else:
            break
            
    print(height)

if __name__ == "__main__":
    solve()