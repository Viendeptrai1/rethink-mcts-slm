import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        R = int(next(iterator))
        S = int(next(iterator))
    except StopIteration:
        return

    matrix = []
    for _ in range(R):
        row = []
        for _ in range(S):
            row.append(int(next(iterator)))
        matrix.append(row)

    # If dimensions are less than 2x2, no extremely cool submatrix exists
    if R < 2 or S < 2:
        print(0)
        return

    # Precompute a boolean matrix 'valid' where valid[i][j] is True if the 2x2 submatrix
    # with top-left at (i, j) is "cool".
    # The condition for a 2x2 submatrix with corners (r1, c1), (r1, c2), (r2, c1), (r2, c2)
    # to be cool is: A[r1][c1] + A[r2][c2] <= A[r1][c2] + A[r2][c1]
    # Here, r2 = r1 + 1, c2 = c1 + 1.
    
    # valid[i][j] corresponds to the 2x2 block starting at row i, col j.
    # Dimensions of valid will be (R-1) x (S-1).
    valid = [[False] * (S - 1) for _ in range(R - 1)]
    
    for i in range(R - 1):
        for j in range(S - 1):
            r1, c1 = i, j
            r2, c2 = i + 1, j + 1
            if matrix[r1][c1] + matrix[r2][c2] <= matrix[r1][c2] + matrix[r2][c1]:
                valid[i][j] = True

    # We need to find the largest rectangle of True values in the 'valid' matrix.
    # If we have a rectangle of True values from row r1 to r2 and col c1 to c2 in 'valid',
    # it implies that every 2x2 submatrix within the corresponding region in 'matrix' is cool.
    # However, the problem states a submatrix is "extremely cool" if EACH of its submatrices
    # with at least 2 rows and 2 columns is cool.
    #
    # Let the candidate submatrix in 'matrix' be defined by top-left (R_start, C_start)
    # and bottom-right (R_end, C_end).
    # The condition requires that for ANY r, s such that R_start < r <= R_end and C_start < s <= C_end,
    # the 2x2 submatrix defined by rows (r-1, r) and cols (c-1, c) is cool?
    # Actually, the definition says: "each of its submatrices with at least two rows and two columns is cool".
    # A submatrix of the candidate is defined by its own top-left and bottom-right.
    # Let the candidate be M' with rows r1..r2 and cols c1..c2.
    # Any submatrix of M' with rows r_a..r_b and cols c_a..c_b (where r_b - r_a >= 1 and c_b - c_a >= 1)
    # must satisfy the cool condition: M'[r_a][c_a] + M'[r_b][c_b] <= M'[r_a][c_b] + M'[r_b][c_a].
    #
    # This is the definition of a Monge array (specifically, a Monge matrix where the inequality is <=).
    # A matrix is Monge if and only if all its 2x2 submatrices satisfy the condition.
    # Proof: If all 2x2 submatrices satisfy the condition, then by induction any larger submatrix
    # satisfies the condition. Conversely, if a larger submatrix satisfies it, does it imply 2x2?
    # Yes, because a larger submatrix includes the 2x2 ones as submatrices.
    # Therefore, the condition "every submatrix with >=2 rows and >=2 cols is cool" is equivalent to
    # "every 2x2 submatrix is cool".
    #
    # So the problem reduces to: Find the largest rectangle in the 'valid' boolean matrix such that
    # all entries in that rectangle are True.
    # The size of the resulting submatrix in 'matrix' will be:
    # (number of rows in valid rectangle + 1) * (number of cols in valid rectangle + 1).
    # If the valid rectangle spans rows i1 to i2 (inclusive) and cols j1 to j2 (inclusive),
    # then the rows in matrix are from i1 to i2+1, count = i2 - i1 + 2.
    # Similarly for columns.
    
    # Algorithm: Maximum Rectangle in Binary Matrix
    # We can use the histogram method.
    # For each row i in 'valid', we compute the height of consecutive True values ending at i.
    # Then find the largest rectangle in the histogram.
    
    max_area = 0
    heights = [0] * (S - 1)
    
    for i in range(R - 1):
        for j in range(S - 1):
            if valid[i][j]:
                heights[j] += 1
            else:
                heights[j] = 0
        
        # Calculate max rectangle in histogram 'heights'
        # Using a stack-based approach O(S)
        stack = [] # stores indices
        for j in range(S):
            # We append a sentinel at the end or handle loop carefully.
            # Let's iterate j from 0 to S-1.
            # To handle the remaining elements in stack, we can imagine a height of 0 at index S.
            current_h = heights[j] if j < S - 1 else 0
            
            while stack and (current_h < heights[stack[-1]]):
                h = heights[stack.pop()]
                w = j if not stack else j - stack[-1] - 1
                area = h * w
                if area > max_area:
                    max_area = area
            stack.append(j)
        
        # Note: The loop above goes up to S-1. The sentinel logic inside handles the pop.
        # But we need to ensure we process the last element correctly if it's part of a rectangle.
        # The standard way is to iterate j from 0 to S (inclusive) with heights[S] = 0.
        # Let's refactor the inner loop slightly for clarity and correctness.
    
    # Re-doing the histogram part cleanly inside the row loop
    for i in range(R - 1):
        # Update heights for current row
        for j in range(S - 1):
            if valid[i][j]:
                heights[j] += 1
            else:
                heights[j] = 0
        
        # Find max rectangle in current histogram
        stack = []
        # Iterate j from 0 to S-1, and treat index S as having height 0 to flush stack
        for j in range(S):
            h = heights[j] if j < S - 1 else 0
            while stack and h < heights[stack[-1]]:
                height = heights[stack.pop()]
                width = j if not stack else j - stack[-1] - 1
                area = height * width
                if area > max_area:
                    max_area = area
            stack.append(j)

    # max_area is the number of 2x2 blocks.
    # If max_area is 0, no extremely cool submatrix exists.
    if max_area == 0:
        print(0)
    else:
        # The dimensions of the submatrix in 'matrix' are:
        # rows = max_area_rows + 1
        # cols = max_area_cols + 1
        # But we only have the area. We need the max possible (rows * cols).
        # Wait, the question asks for the "largest number of elements".
        # This is simply the area of the submatrix in terms of elements.
        # If the rectangle of 2x2 blocks has height H and width W (in terms of blocks),
        # then the number of rows in the matrix submatrix is H + 1.
        # The number of columns is W + 1.
        # Total elements = (H + 1) * (W + 1).
        # However, our 'max_area' variable stores H * W.
        # We need to maximize (H+1)*(W+1) subject to H*W = max_area?
        # No. The algorithm finds the maximum H*W. But different (H, W) pairs can yield different (H+1)*(W+1).
        # Example: H=2, W=3 -> Area=6, Elements=(3)*(4)=12.
        #          H=1, W=6 -> Area=6, Elements=(2)*(7)=14.
        # So we cannot just take max_area and derive the answer.
        # We must track the maximum (H+1)*(W+1) directly.
        
        # Let's re-run the histogram logic but maximize (h+1)*(w+1) instead of h*w.
        pass

    # Re-implementing the loop to maximize (h+1)*(w+1)
    max_elements = 0
    heights = [0] * (S - 1)
    
    for i in range(R - 1):
        for j in range(S - 1):
            if valid[i][j]:
                heights[j] += 1
            else:
                heights[j] = 0
        
        stack = []
        for j in range(S):
            h = heights[j] if j < S - 1 else 0
            while stack and h < heights[stack[-1]]:
                height = heights[stack.pop()]
                width = j if not stack else j - stack[-1] - 1
                # Number of rows in matrix submatrix = height + 1
                # Number of cols in matrix submatrix = width + 1
                elements = (height + 1) * (width + 1)
                if elements > max_elements:
                    max_elements = elements
            stack.append(j)

    print(max_elements)

if __name__ == '__main__':
    solve()