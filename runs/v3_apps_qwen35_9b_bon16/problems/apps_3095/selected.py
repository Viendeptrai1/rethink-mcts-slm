import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        R = int(next(iterator))
        S = int(next(iterator))
    except StopIteration:
        return

    A = []
    for _ in range(R):
        row = []
        for _ in range(S):
            row.append(int(next(iterator)))
        A.append(row)

    # Check for 2x2 submatrices
    # A 2x2 submatrix with top-left at (i, j) is cool if:
    # A[i][j] + A[i+1][j+1] <= A[i][j+1] + A[i+1][j]
    # which rearranges to: A[i][j] - A[i][j+1] - A[i+1][j] + A[i+1][j+1] <= 0

    valid_2x2 = [[False] * (S - 1) for _ in range(R - 1)]
    for i in range(R - 1):
        for j in range(S - 1):
            if A[i][j] + A[i+1][j+1] <= A[i][j+1] + A[i+1][j]:
                valid_2x2[i][j] = True

    # If no 2x2 submatrix is valid, the answer is 0
    # However, we need to find the largest submatrix where EVERY 2x2 inside it is valid.
    # This is equivalent to finding the largest rectangle of True values in valid_2x2 grid,
    # but with a twist: the rectangle in valid_2x2 corresponds to a submatrix in A that is (h+1)x(w+1).
    # Specifically, a submatrix in A from row r1 to r2 and col c1 to c2 (inclusive) is extremely cool
    # if for all i in [r1, r2-1] and j in [c1, c2-1], the 2x2 at (i,j) is valid.
    # This means valid_2x2[i][j] must be True for all those indices.
    # So we need the largest rectangle of Trues in the (R-1)x(S-1) valid_2x2 matrix.
    # The area of the resulting submatrix in A will be (height_rect + 1) * (width_rect + 1).

    if R < 2 or S < 2:
        print(0)
        return

    # Maximal rectangle of 1s in a binary matrix problem
    # valid_2x2 is our binary matrix (1 for True, 0 for False)
    # We compute histogram heights for each row and find max rectangle area in histogram.

    max_elements = 0

    heights = [0] * S
    # Initialize heights based on the first row of valid_2x2? 
    # No, let's build row by row.
    # The binary matrix is (R-1) rows x (S-1) cols.
    # Let's iterate through each row of valid_2x2.

    for i in range(R - 1):
        for j in range(S - 1):
            if valid_2x2[i][j]:
                heights[j] += 1
            else:
                heights[j] = 0

        # Now find largest rectangle in histogram 'heights'
        # Standard O(S) algorithm using stack
        stack = []  # stores indices
        for idx in range(S):
            while stack and heights[stack[-1]] > heights[idx]:
                h = heights[stack.pop()]
                w = idx if not stack else idx - stack[-1] - 1
                area = h * w
                if area > max_elements:
                    max_elements = area
            stack.append(idx)

        while stack:
            h = heights[stack.pop()]
            w = S if not stack else S - 1 - stack[-1]
            area = h * w
            if area > max_elements:
                max_elements = area

    # If max_elements (in terms of 2x2 blocks) is 0, it means no 2x2 submatrix is valid.
    # In that case, output 0.
    # If max_elements > 0, say we found a rectangle of H blocks high and W blocks wide.
    # The actual submatrix in A has dimensions (H+1) x (W+1).
    # Number of elements = (H+1) * (W+1) = H*W + H + W + 1.
    
    if max_elements == 0:
        print(0)
    else:
        H = max_elements  # This variable name is confusing. Let's recalculate.
        # The variable max_elements holds the area of the rectangle in the valid_2x2 grid.
        # Let that area be Area_2x2.
        # We need to recover dimensions H_rect and W_rect such that H_rect * W_rect = Area_2x2.
        # But wait, the histogram method gives us the max area, but not necessarily the dimensions directly.
        # However, if we have a rectangle of height h and width w in the valid_2x2 grid,
        # the submatrix in A has height h+1 and width w+1.
        # The area in A is (h+1)*(w+1).
        # The histogram algorithm finds max (h*w). Does max (h*w) correspond to max ((h+1)*(w+1))?
        # Not necessarily. Example: h=1, w=10 -> h*w=10, (h+1)*(w+1)=22.
        # h=5, w=2 -> h*w=10, (h+1)*(w+1)=18.
        # So we cannot just use the area from the histogram. We need to track the dimensions.
        
        # Let's re-run the histogram logic but store (h, w) pairs and maximize (h+1)*(w+1).
        # Or better, just re-implement the histogram part to track dimensions.

        best_area = 0
        heights = [0] * S
        
        for i in range(R - 1):
            for j in range(S - 1):
                if valid_2x2[i][j]:
                    heights[j] += 1
                else:
                    heights[j] = 0
            
            stack = []
            for idx in range(S):
                while stack and heights[stack[-1]] > heights[idx]:
                    h = heights[stack.pop()]
                    w = idx if not stack else idx - stack[-1] - 1
                    # Update best with dimensions h x w in valid_2x2 grid
                    # Corresponds to (h+1) x (w+1) in A
                    current_elements = (h + 1) * (w + 1)
                    if current_elements > best_area:
                        best_area = current_elements
                stack.append(idx)

            while stack:
                h = heights[stack.pop()]
                w = S if not stack else S - 1 - stack[-1]
                current_elements = (h + 1) * (w + 1)
                if current_elements > best_area:
                    best_area = current_elements

        print(best_area)

if __name__ == '__main__':
    solve()