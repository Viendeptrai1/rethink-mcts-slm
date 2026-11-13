import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return

    # Parse the expression into numbers and operators
    nums = []
    ops = []
    curr = ""
    for char in s:
        if char.isdigit():
            curr += char
        else:
            nums.append(int(curr))
            ops.append(char)
            curr = ""
    nums.append(int(curr))

    n = len(nums)
    m = len(ops)
    
    # Identify positions of multiplication signs
    mul_indices = []
    for i in range(m):
        if ops[i] == '*':
            mul_indices.append(i)
    
    if not mul_indices:
        # No multiplication signs, adding brackets won't change the sum
        print(sum(nums))
        return

    # Since the number of * signs is at most 15, we can try all possible pairs
    # of (i, j) where i and j are indices in the ops array (0-based) such that
    # we place brackets around the sub-expression from nums[i] to nums[j+1].
    # The expression becomes: (nums[i] op[i] ... op[j] nums[j+1]) combined with the rest.
    
    # Precompute prefix sums and products to quickly evaluate segments without re-running big arithmetic.
    # However, since the segment inside brackets might contain mixed + and *, we need to evaluate it carefully.
    # Given constraints: total length up to 5001, but only 15 '*' signs.
    # The segment inside brackets will contain at least one '*' (otherwise it's just a sum, and brackets don't change anything for addition only segments unless they interact with surrounding *).
    # Actually, the optimal placement usually involves enclosing a segment that contains a '*' to leverage operator precedence.
    
    # We will iterate over all possible start and end positions for the bracketed part.
    # A bracketed part covers nums[i] through nums[j+1] and operators ops[i]...ops[j].
    # Let's define i as the index of the first number included, and j as the index of the last operator included.
    # Then the segment is nums[i] op[i] ... op[j] nums[j+1].
    # Valid i ranges from 0 to m-1. Valid j ranges from i to m-1.
    
    # To optimize, note that if the segment inside brackets has no '*', then (A+B+C) is same as A+B+C.
    # The value changes only if the bracketed segment is multiplied by something on the left or right.
    # So we only need to consider segments that either:
    # 1. Are adjacent to a '*' on the left (i.e., ops[i-1] == '*') OR
    # 2. Are adjacent to a '*' on the right (i.e., ops[j+1] == '*') OR
    # 3. Contain at least one '*' internally (which they will if they span across a mul index).
    
    # Actually, simpler approach given N=15 mul signs:
    # The expression can be viewed as a product of terms separated by '+'.
    # Example: A + B * C * D + E * F ...
    # If we put brackets, we are essentially changing the order of operations for a sub-segment.
    # The most impactful change happens when we turn a sum into a factor of a larger product.
    # E.g., ... * (X + Y) * ...
    # Or ... (X + Y) * ...
    # Or ... * (X * Y * ...)
    
    # Since the number of * is small (<=15), the total number of multiplicative blocks is small.
    # We can split the original expression by '+' into chunks. Each chunk is a product of numbers.
    # Let the chunks be C1, C2, ..., Ck. The expression is C1 + C2 + ... + Ck.
    # If we don't add brackets, value = sum(Ci).
    # If we add brackets around a sub-segment, we are effectively taking a sub-segment of one or more chunks,
    # computing its value with new precedence (which usually means doing sums inside first if we break a product),
    # and then combining with the rest.
    
    # Let's parse into chunks separated by '+'.
    chunks = []
    current_chunk_nums = []
    current_chunk_ops = [] # operators inside the chunk (all must be '*')
    
    for i in range(m):
        if ops[i] == '+':
            # Finish current chunk
            if current_chunk_nums:
                chunks.append(current_chunk_nums)
                current_chunk_nums = []
            current_chunk_ops = []
        else:
            current_chunk_nums.append(nums[i])
            current_chunk_ops.append(ops[i])
    # Add last chunk
    if current_chunk_nums:
        chunks.append(current_chunk_nums)

    # Now we have a list of chunks. Each chunk is a list of numbers connected by '*'.
    # The original value is sum(chunk_eval(c) for c in chunks).
    # We need to pick a range [i, j] of chunks (or parts within chunks) to wrap in brackets.
    # But actually, the bracket can start and end anywhere.
    # However, the logic simplifies if we consider that the bracketed segment will be evaluated 
    # according to standard precedence EXCEPT that the + inside the brackets (if any) are done first?
    # No, the problem says "add one pair of brackets". The rest follows standard precedence.
    # So if we have A * (B + C) * D, the + is evaluated first.
    # If we have (A + B) * C, + is evaluated first.
    # If we have A * B * (C + D), + is evaluated first.
    # If we have A + B * (C + D) * E, the inner (C+D) is evaluated, then multiplied by B and E, then added to A.
    
    # Strategy:
    # Iterate over all possible start indices (s_idx) and end indices (e_idx) in the original operator list.
    # s_idx: index of the first operator included in the bracket.
    # e_idx: index of the last operator included in the bracket.
    # The bracketed part covers nums[s_idx] ... ops[e_idx] ... nums[e_idx+1].
    # Wait, if we start bracket at a number, the first operator is the one after it.
    # Let's define the bracketed segment by the range of operators [i, j].
    # This segment includes nums[i], ops[i]...ops[j], nums[j+1].
    # We evaluate this segment with standard precedence (so * before +).
    # Then we replace this segment with its result in the original expression and evaluate the whole thing.
    
    # Optimization: Since * count is small, the expression has few '*' operations.
    # The segment we bracket might be large, but the number of '*' inside is small.
    # The number of '+' inside can be large.
    # Evaluating a segment with many '+' and few '*' is fast if we handle it right.
    # Actually, any segment with only '+' is just a sum.
    # A segment with '+' and '*' is evaluated by splitting at '+' and multiplying the resulting sums?
    # No, standard precedence: * binds tighter. So A + B * C = A + (B*C).
    # So to evaluate a segment, we can split it by '+' first, getting terms, then evaluate each term (which is a product), then sum them.
    
    # Let's implement a function to evaluate a segment defined by nums range [l, r] and ops range [l, r-1].
    # But since we are modifying the expression by replacing a subsegment, we need to be careful.
    # Instead of full re-evaluation (which is O(N)), we can do it in O(N) total since we do it once per pair?
    # Pairs of (i, j) where 0 <= i <= j < m. That's O(m^2) ~ 15^2 = 225.
    # O(N) per pair is 5000. Total operations ~ 1e6, which is fine for Python.
    
    def evaluate_segment(nums_list, ops_list):
        # nums_list: list of numbers in the segment
        # ops_list: list of operators in the segment (same length as nums_list - 1)
        # Evaluate with standard precedence: * before +
        
        # Split by '+'
        terms = []
        current_term_nums = []
        current_op = None
        
        for idx, op in enumerate(ops_list):
            num = nums_list[idx]
            if op == '+':
                # Finish current term
                if current_term_nums:
                    term_val = 1
                    for x in current_term_nums:
                        term_val *= x
                    terms.append(term_val)
                current_term_nums = [num]
            else:
                # op is '*'
                current_term_nums.append(num)
        # Last term
        if current_term_nums:
            term_val = 1
            for x in current_term_nums:
                term_val *= x
            terms.append(term_val)
        
        return sum(terms)

    # We need to handle the case where the bracketed segment starts at a number or ends at a number.
    # The bracketed segment is defined by the range of operators [i, j].
    # This corresponds to numbers: nums[i] ... nums[j+1].
    # Operators: ops[i] ... ops[j].
    # i can range from 0 to m-1.
    # j can range from i to m-1.
    # But we can also have a bracket around a single number? e.g. (3). That doesn't change anything.
    # Or around a single operation? (3*4). That doesn't change anything unless it changes precedence with neighbors.
    # But (3*4) is same as 3*4. The only time brackets matter is if they change the order of + and *.
    # Specifically, if we have ... * (A + B) * ... or (A + B) * ...
    # Or if we have ... + (A * B) * ... (no change).
    # So we only need to consider segments that contain at least one '+' AND at least one '*'?
    # Not necessarily. If we have A * B + C * D, and we do (A * B) + (C * D), no change.
    # If we do A * (B + C) * D, we change B*C*D to (B+C)*D.
    # If we do (A + B) * C, we change A*B*C to (A+B)*C.
    # If we do A + (B + C) * D, no change (sum inside brackets doesn't help).
    # So the bracketed segment must be such that the internal evaluation order is different from external.
    # This happens if the segment contains a '+' and is adjacent (left or right) to a '*', OR contains a '*' and is adjacent to a '+'.
    # Actually, simpler: just try all valid (i, j) pairs. The O(N) evaluation is cheap enough.
    
    max_val = 0
    
    # Try all possible bracket positions
    # i is the index of the first operator included in the bracket.
    # j is the index of the last operator included in the bracket.
    # The segment is nums[i] ... nums[j+1].
    # If i == j+1 (i.e., only one number), it's trivial.
    
    # To cover all cases:
    # Case 1: Bracket covers operators from i to j.
    # Case 2: What if we bracket just one number? (nums[k]). No change.
    # Case 3: What if we bracket a segment starting before an operator but not including the previous operator?
    # My definition of [i, j] covers exactly the sub-expression nums[i] op[i] ... op[j] nums[j+1].
    # This covers any contiguous sub-expression that starts with a number and ends with a number.
    # Does it cover (nums[k])? Yes, if we consider i such that ops[i] is the one after nums[k], but we don't include it.
    # Wait, if I choose i=k, j=k-1? No, i must be <= j.
    # If I want to bracket just nums[k], that's equivalent to bracketing nums[k]...nums[k], which is a single term.
    # The value of a single term is the number itself. Replacing it with itself changes nothing.
    # So we can skip single-number brackets.
    # We need at least one operator inside. So j >= i.
    
    for i in range(m):
        for j in range(i, m):
            # Segment: nums[i] ... nums[j+1]
            # Operators: ops[i] ... ops[j]
            
            # Extract segment
            seg_nums = nums[i : j+2]
            seg_ops = ops[i : j+1]
            
            seg_val = evaluate_segment(seg_nums, seg_ops)
            
            # Now reconstruct the expression value
            # We have segments:
            # Part 1: nums[0] ... nums[i-1]
            # Part 2: seg_val
            # Part 3: nums[j+2] ... nums[n-1]
            # Operators connecting them:
            # Left part ops: 0 to i-2
            # Right part ops: j+1 to m-1
            # Connection between Part 1 and Part 2 is ops[i-1] (if i>0)
            # Connection between Part 2 and Part 3 is ops[j+1] (if j+1 < m)
            
            # Let's build the full list of numbers and operators for the new expression
            new_nums = []
            new_ops = []
            
            # Left part
            if i > 0:
                new_nums.extend(nums[0:i])
                new_ops.extend(ops[0:i-1])
                # The operator between left part and segment is ops[i-1]
                new_ops.append(ops[i-1])
                new_nums.append(seg_val)
            else:
                # Segment is at the very beginning
                new_nums.append(seg_val)
            
            # Right part
            # The operator between segment and right part is ops[j+1] (if exists)
            if j + 1 < m:
                if i > 0:
                    # We already added seg_val and ops[i-1] to new_nums/new_ops
                    # Now add the connecting op between segment and right part
                    new_ops.append(ops[j+1])
                else:
                    # Segment at start, no left op yet
                    new_ops.append(ops[j+1])
                new_nums.extend(nums[j+2:])
            else:
                # Segment at the very end
                if i > 0:
                    # Already added seg_val and ops[i-1]
                    pass
                else:
                    # Just seg_val
                    pass
            
            # Evaluate the new expression
            # new_nums and new_ops form a valid expression
            total_val = evaluate_segment(new_nums, new_ops)
            if total_val > max_val:
                max_val = total_val

    # There is one edge case: what if the optimal solution is just the original expression?
    # The problem says "add one pair of brackets". Even if it doesn't change value, it's valid.
    # Our loop covers cases where brackets don't change value (e.g., single number, or (A*B) where no + involved).
    # But we initialized max_val = 0. If the expression is all positive, max_val will be updated.
    # However, we should also consider the case where we don't effectively change anything but it's allowed.
    # Actually, our loop covers (A*B) as a segment with one op. 
    # If the expression is "3*4*5", our loop will try i=0, j=0 -> (3*4)*5, i=0,j=1 -> (3*4*5), etc.
    # So it should be covered.
    
    # Wait, what if the expression is just a single number? "5".
    # Then m=0, loops don't run.
    # If m=0, we should output the number.
    if m == 0:
        print(sum(nums)) # Just the number
        return
    
    print(max_val)

solve()