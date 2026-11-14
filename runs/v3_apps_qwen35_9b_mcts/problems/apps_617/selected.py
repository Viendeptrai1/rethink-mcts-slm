import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return

    nums = []
    ops = []
    current_num = 0
    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        else:
            nums.append(current_num)
            ops.append(char)
            current_num = 0
    nums.append(current_num)

    n = len(nums)
    max_val = 0

    # Iterate over all possible pairs of indices (i, j) to place brackets around nums[i]...nums[j]
    # The brackets will enclose the sub-expression from index i to j inclusive.
    # This means we calculate the value of the sub-expression nums[i] op[i] ... op[j-1] nums[j]
    # and then evaluate the whole expression treating that result as a single number.
    
    for i in range(n):
        for j in range(i, n):
            # Create a copy of nums and ops to simulate the bracketed evaluation
            # We will compute the value of the segment from i to j first.
            
            # Segment numbers: nums[i] ... nums[j]
            # Segment operators: ops[i] ... ops[j-1]
            
            # Evaluate the segment with standard precedence (no brackets inside, just normal math)
            # But wait, the problem says "add one pair of brackets". The content inside the brackets
            # is evaluated first. The content inside is a sequence of numbers and operators.
            # We must evaluate that inner sequence with standard precedence (multiplication before addition).
            
            inner_nums = nums[i : j+1]
            inner_ops = ops[i : j]
            
            # Evaluate inner expression
            if not inner_ops:
                inner_val = inner_nums[0]
            else:
                # First pass: handle multiplications
                stack = [inner_nums[0]]
                for k in range(len(inner_ops)):
                    op = inner_ops[k]
                    next_val = inner_nums[k+1]
                    if op == '*':
                        stack[-1] *= next_val
                    else:
                        stack.append(next_val)
                # Second pass: handle additions
                result = 0
                for val in stack:
                    result += val
                inner_val = result
            
            # Now evaluate the full expression with inner_val replacing the segment
            # Full expression structure:
            # nums[0] ... ops[i-1] [inner_val] ops[j] ... nums[n-1]
            
            # Construct new lists
            new_nums = nums[:i] + [inner_val] + nums[j+1:]
            new_ops = ops[:i] + ops[j:]
            
            # Evaluate the new expression with standard precedence
            if not new_ops:
                final_val = new_nums[0]
            else:
                # Handle multiplications
                stack = [new_nums[0]]
                for k in range(len(new_ops)):
                    op = new_ops[k]
                    next_val = new_nums[k+1]
                    if op == '*':
                        stack[-1] *= next_val
                    else:
                        stack.append(next_val)
                # Handle additions
                result = 0
                for val in stack:
                    result += val
                final_val = result
            
            if final_val > max_val:
                max_val = final_val

    print(max_val)

if __name__ == "__main__":
    solve()