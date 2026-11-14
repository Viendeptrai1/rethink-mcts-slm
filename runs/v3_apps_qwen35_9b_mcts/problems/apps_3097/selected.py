import sys
from bisect import bisect_right, bisect_left

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        Q = int(next(iterator))
    except StopIteration:
        return

    queries = []
    max_val = 0
    for _ in range(Q):
        a = int(next(iterator))
        b = int(next(iterator))
        queries.append((a, b))
        if b > max_val:
            max_val = b

    # We need to collect all numbers in the table that are <= max_val.
    # The table is defined by:
    # A(i, 1) = i
    # A(i, j) = A(i, j-1) + rev(A(i, j-1))
    # We iterate over rows i starting from 1.
    # For each row, we generate the sequence until the value exceeds max_val.
    # Since the sequence grows very fast (roughly doubling the number of digits or adding significant magnitude),
    # the total number of elements across all rows up to 10^10 is manageable.
    
    all_numbers = []
    
    i = 1
    while True:
        # Start of row i
        current = i
        if current > max_val:
            break
        
        # Add the first element
        all_numbers.append(current)
        
        # Generate subsequent elements
        while True:
            s = str(current)
            rev_s = s[::-1]
            rev_val = int(rev_s)
            next_val = current + rev_val
            
            if next_val > max_val:
                break
            
            all_numbers.append(next_val)
            current = next_val
        
        # Check if the starting number of the next row will exceed max_val
        # Since A(i, 1) = i, if i > max_val, we stop.
        i += 1
        if i > max_val:
            break

    # Sort the collected numbers to allow binary search
    all_numbers.sort()

    results = []
    for a, b in queries:
        # Count numbers in [a, b]
        # count = count(<= b) - count(<= a-1)
        idx_b = bisect_right(all_numbers, b)
        idx_a = bisect_left(all_numbers, a)
        count = idx_b - idx_a
        results.append(str(count))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()