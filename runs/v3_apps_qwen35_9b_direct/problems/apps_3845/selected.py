import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])

    # We will construct a grid of size (A+B) x (A+B)
    # Strategy:
    # Create a diagonal pattern where we place white components along the main diagonal
    # and black components along the anti-diagonal or interleaved in a way that they don't touch.
    # However, a simpler and more robust construction for competitive programming:
    # Use a grid where we place A white components and B black components such that they are isolated.
    #
    # Construction idea:
    # Let h = A + B, w = A + B.
    # We can place the A white components at positions (i, i) for i in 0..A-1.
    # We can place the B black components at positions (i, i+A) for i in 0..B-1.
    # But we must ensure they don't touch.
    #
    # Better construction:
    # Create a grid where we have a "staircase" of white components and a "staircase" of black components
    # separated by a buffer or arranged such that they never touch.
    #
    # Let's try this specific layout:
    # Grid size: (A+B) x (A+B)
    # For row i from 0 to A-1:
    #   Place a white component at (i, i). To make it a component of size 1, we just put '.' there.
    #   But we need to ensure it doesn't connect to other white cells. So we put '#' around it if necessary.
    #   Actually, if we put '.' at (i,i) and '#' everywhere else in that row/col except specific spots,
    #   we can isolate them.
    #
    # Simpler approach used in similar problems:
    # Create a grid where we have A white single-cell components and B black single-cell components.
    # Arrange them in a way that no two white cells are adjacent and no two black cells are adjacent.
    # And also no white is adjacent to a black? No, white and black can be adjacent, that's fine.
    # The constraint is:
    # - White components must be disconnected from each other.
    # - Black components must be disconnected from each other.
    # - White and Black can touch.
    #
    # So we just need to ensure:
    # 1. No two white cells are adjacent (4-connectivity).
    # 2. No two black cells are adjacent (4-connectivity).
    #
    # If we satisfy these two, then each white cell is its own component (count = number of white cells)
    # and each black cell is its own component (count = number of black cells).
    #
    # How to arrange A white and B black cells on a grid such that no two same-colored cells are adjacent?
    # We can use a checkerboard-like pattern but with more flexibility.
    # Or simply place them far apart.
    #
    # Let's use a grid of size (A+B) x (A+B).
    # Place white cells at (i, 2*i) for i in 0..A-1? No, might get too wide.
    #
    # Alternative:
    # Place white cells at (i, i) for i in 0..A-1.
    # Place black cells at (i, i+A) for i in 0..B-1.
    # Check adjacency:
    # White at (i, i). Neighbors: (i-1, i), (i+1, i), (i, i-1), (i, i+1).
    # Black at (j, j+A).
    # Can a white cell be adjacent to a black cell? Yes, but that's allowed.
    # Can a white cell be adjacent to another white cell?
    #   White at (i, i) and (k, k). They are adjacent if |i-k| + |i-k| = 1 => |i-k|=0.5 impossible.
    #   Or if they share a row/col and are next to each other.
    #   In row i, white is at col i. In row i+1, white is at col i+1.
    #   Distance between (i, i) and (i+1, i+1) is 2 (diagonal), not adjacent.
    #   Distance between (i, i) and (i, i+1)? No, because next white is at (i+1, i+1).
    #   So white cells are never adjacent.
    # Similarly for black cells at (j, j+A).
    #   Black at (j, j+A) and (k, k+A).
    #   Same logic: diagonal distance 2, no row/col adjacency.
    #
    # So this layout works:
    # Grid size: max(A, B) + max(A, B) ? No.
    # We need rows 0..A-1 and cols 0..A-1 for white.
    # We need rows 0..B-1 and cols A..A+B-1 for black.
    # So total rows = max(A, B). Total cols = A + B.
    # But we need to handle the case where A != B.
    #
    # Let's set:
    # h = A + B
    # w = A + B
    #
    # Place white at (i, i) for i in 0..A-1.
    # Place black at (i, i+A) for i in 0..B-1.
    #
    # Check bounds:
    # White: row i < A, col i < A. OK.
    # Black: row i < B, col i+A < A+B. OK.
    #
    # Are any white cells adjacent?
    #   (i, i) and (i+1, i+1): dx=1, dy=1 -> not adjacent.
    #   (i, i) and (i, i+1): no white at (i, i+1).
    #   (i, i) and (i-1, i-1): same.
    #   (i, i) and (i+1, i): no white at (i+1, i).
    #   So no white-white adjacency.
    #
    # Are any black cells adjacent?
    #   (i, i+A) and (i+1, i+1+A): dx=1, dy=1 -> not adjacent.
    #   (i, i+A) and (i, i+1+A): no black at (i, i+1+A).
    #   So no black-black adjacency.
    #
    # Therefore, we have exactly A white components and B black components.
    #
    # Fill the grid:
    # Initialize with '#'.
    # Set (i, i) = '.' for i in 0..A-1.
    # Set (i, i+A) = '.' for i in 0..B-1.
    #
    # Print h and w, then the grid.

    h = A + B
    w = A + B
    
    grid = [['#' for _ in range(w)] for _ in range(h)]
    
    for i in range(A):
        grid[i][i] = '.'
    
    for i in range(B):
        grid[i][i + A] = '.'
        
    print(f"{h} {w}")
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    solve()