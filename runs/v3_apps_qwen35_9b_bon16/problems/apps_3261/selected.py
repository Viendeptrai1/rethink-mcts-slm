import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    R = int(input_data[0])
    C = int(input_data[1])
    K = int(input_data[2])
    
    # The hedgehog moves in a zig-zag pattern starting from (0,0).
    # The path fills the board row by row and column by column in a specific order.
    # Let's determine the order:
    # It starts at (0,0).
    # In the first "layer" (max(row, col) = 0), we have (0,0).
    # In the second "layer" (max(row, col) = 1), we have (0,1) and (1,0).
    # In the third "layer" (max(row, col) = 2), we have (1,2), (2,1), (0,2) ? 
    # Wait, let's re-examine the standard zig-zag (like reading a wave).
    # Usually, these problems refer to the pattern where we traverse diagonals.
    # Diagonal d = r + c.
    # d=0: (0,0) -> 1 cell
    # d=1: (0,1), (1,0) -> 2 cells
    # d=2: (2,0), (1,1), (0,2) OR (0,2), (1,1), (2,0)?
    # The problem says "zig-zag pattern as in the second image". Since I cannot see the image,
    # I must infer from the logic of such problems or the examples.
    
    # Let's trace Example 1: R=10, C=10, K=6. Output=5.
    # Cells:
    # (0,0): white (0&0=0? No, condition is "at least one digit 1 in the same position". 
    # Binary: 0 & 0 -> 0 ones in common. So GREY.
    # (0,1): 0 (00) and 1 (01). No common 1. GREY.
    # (0,2): 0 (00) and 2 (10). No common 1. GREY.
    # ...
    # (4,5): 4 is 100, 5 is 101. Common bit at pos 2 (value 4). WHITE.
    # (2,5): 2 is 010, 5 is 101. No common bit. GREY.
    
    # Definition of White: popcount(row & col) > 0.
    # Definition of Grey: popcount(row & col) == 0.
    # (0,0): 0 & 0 = 0. popcount=0. GREY.
    
    # Hypothesis for path: Diagonals d = r + c.
    # Direction alternates.
    # d=0: (0,0) -> 1 cell. Total=1.
    # d=1: (0,1), (1,0). Which order?
    # If (0,1), (1,0):
    #   (0,1): grey. (1,0): grey.
    #   Sequence: (0,0), (0,1), (1,0), ...
    # d=2: (2,0), (1,1), (0,2) or reverse?
    # If pattern is: d even -> bottom-left to top-right? d odd -> top-right to bottom-left?
    # Or based on standard "diagonal traversal":
    # d=0: (0,0)
    # d=1: (0,1), (1,0)
    # d=2: (2,0), (1,1), (0,2)  <- This is one common pattern (downward then upward?)
    # Actually, standard zig-zag often goes:
    # (0,0)
    # (0,1), (1,0)
    # (2,0), (1,1), (0,2)
    # (0,3), (1,2), (2,1), (3,0)
    # ...
    # Let's check counts.
    # d=0: 1 cell. Cum: 1.
    # d=1: 2 cells. Cum: 3.
    # d=2: 3 cells. Cum: 6.
    # K=6 covers d=0, d=1, d=2 completely.
    # Cells: (0,0), (0,1), (1,0), (2,0), (1,1), (0,2).
    # Colors:
    # (0,0): 0&0=0 -> Grey.
    # (0,1): 0&1=0 -> Grey.
    # (1,0): 1&0=0 -> Grey.
    # (2,0): 2&0=0 -> Grey.
    # (1,1): 1&1=1 -> White.
    # (0,2): 0&2=0 -> Grey.
    # Grey count: 5.
    # Matches Sample 1 output (5).
    
    # So the pattern is:
    # Diagonal d = r + c.
    # If d is even: traverse from r = min(d, R-1) down to max(0, d - C + 1). (Bottom-Left to Top-Right? Wait, r decreases)
    #   Actually, if d is even, we start with higher row index?
    #   In my trace above for d=2 (even), I assumed (2,0), (1,1), (0,2). Here r starts at 2, goes to 0.
    #   For d=0 (even), r=0.
    # If d is odd: traverse from r = max(0, d - C + 1) up to min(d, R-1). (Top-Right to Bottom-Left? r increases)
    #   In my trace above for d=1 (odd), I assumed (0,1), (1,0). Here r starts at 0, goes to 1.
    # This matches the "zig-zag" alternating direction.
    
    # Let's verify constraints. R, C up to 10^6. K up to 10^12.
    # We need an O(1) or O(log) solution, not simulation.
    
    def count_grey_in_range(r_start, r_end, c_start, c_end):
        # This function is not needed if we iterate diagonals, but iterating diagonals is O(K) worst case?
        # No, number of diagonals is R+C ~ 2*10^6. This is acceptable for O(N) where N=R+C.
        # K can be large, but we only iterate until we cover K cells.
        # Max diagonals needed is roughly min(R+C, K). Since K <= R*C, but we stop when sum of cells >= K.
        # The number of full diagonals we process is at most R+C.
        # Iterating up to 2*10^6 is fast in Python (1-2 seconds).
        # So we can simulate the diagonals.
        
        total_grey = 0
        curr = 0
        
        d = 0
        while curr < K:
            # Determine the range of r for diagonal d
            # r + c = d => c = d - r
            # Constraints: 0 <= r < R, 0 <= c < C => 0 <= d - r < C => d - C + 1 <= r <= d
            # So r in [max(0, d - C + 1), min(d, R - 1)]
            
            r_min = max(0, d - C + 1)
            r_max = min(d, R - 1)
            
            if r_min > r_max:
                break # Should not happen if d < R+C
            
            count = r_max - r_min + 1
            if curr + count <= K:
                # Full diagonal
                if d % 2 == 0:
                    # Even d: r goes from r_max down to r_min
                    # Cells: (r_max, d-r_max), (r_max-1, d-(r_max-1)), ..., (r_min, d-r_min)
                    for r in range(r_max, r_min - 1, -1):
                        c = d - r
                        if (r & c) == 0:
                            total_grey += 1
                else:
                    # Odd d: r goes from r_min up to r_max
                    # Cells: (r_min, d-r_min), ..., (r_max, d-r_max)
                    for r in range(r_min, r_max + 1):
                        c = d - r
                        if (r & c) == 0:
                            total_grey += 1
                curr += count
            else:
                # Partial diagonal
                remaining = K - curr
                if d % 2 == 0:
                    # r goes from r_max down. We take 'remaining' cells.
                    # Start at r_max, go down 'remaining' steps.
                    # r values: r_max, r_max-1, ..., r_max - remaining + 1
                    for i in range(remaining):
                        r = r_max - i
                        c = d - r
                        if (r & c) == 0:
                            total_grey += 1
                else:
                    # r goes from r_min up. We take 'remaining' cells.
                    # r values: r_min, r_min+1, ..., r_min + remaining - 1
                    for i in range(remaining):
                        r = r_min + i
                        c = d - r
                        if (r & c) == 0:
                            total_grey += 1
                curr = K
                break
            
            d += 1
        
        return total_grey

    print(count_grey_in_range(0, 0, 0, 0))

if __name__ == '__main__':
    solve()