import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    q = int(next(iterator))
    
    # Precompute cumulative lengths of blocks to find which block k falls into.
    # Block i consists of numbers 1, 2, ..., i.
    # We need to find the smallest block index B such that sum(len(block_j) for j in 1..B) >= k.
    # Since k <= 10^9, we can precompute this up to a point where the cumulative sum exceeds 10^9.
    
    # Let's estimate the maximum block index needed.
    # The length of block i is roughly i * log10(i).
    # Sum of lengths up to B is roughly integral of x*log10(x) dx ~ (1/2) B^2 log10(B).
    # If B = 10^5, B^2 = 10^10, log10(B)=5, sum ~ 2.5 * 10^10 > 10^9.
    # So B will be around 10^4 or 10^5. We can safely precompute up to 200,000.
    
    max_k = 10**9
    block_lengths = []
    cumulative_lengths = []
    
    current_block_len = 0
    current_cumulative = 0
    idx = 1
    
    # We generate blocks until cumulative length exceeds max_k
    while current_cumulative <= max_k:
        # Calculate length of block 'idx'
        # Block 'idx' contains numbers 1, 2, ..., idx
        # We need to sum the number of digits for each number from 1 to idx.
        # We can do this efficiently by grouping numbers by digit count.
        
        block_len = 0
        num = 1
        while num <= idx:
            # Determine digit length of 'num'
            d_len = len(str(num))
            # Count how many numbers have this digit length in the range [1, idx]
            # Numbers with d_len digits start from 10^(d_len-1) and go up to 10^d_len - 1
            start = 10**(d_len-1)
            end = 10**d_len - 1
            count = min(idx, end) - start + 1
            if count > 0:
                block_len += count * d_len
            # Move to next digit length group
            num = 10**d_len
            if num > idx:
                break
        
        current_block_len = block_len
        current_cumulative += current_block_len
        block_lengths.append(current_block_len)
        cumulative_lengths.append(current_cumulative)
        idx += 1
        
        # Safety break, though the loop condition should handle it
        if idx > 200000:
            break
            
    results = []
    
    for _ in range(q):
        k = int(next(iterator))
        
        # Find which block k falls into
        # We need the smallest index i such that cumulative_lengths[i] >= k
        # Since cumulative_lengths is sorted, we can use binary search or linear scan (q is small, 500)
        # Linear scan is fine for 500 queries and ~100k blocks, but binary search is better.
        # Let's implement a simple binary search.
        
        low = 0
        high = len(cumulative_lengths) - 1
        block_idx = -1
        
        while low <= high:
            mid = (low + high) // 2
            if cumulative_lengths[mid] >= k:
                block_idx = mid
                high = mid - 1
            else:
                low = mid + 1
        
        # Now we know k is in block_idx (0-based index in our list, corresponding to block number block_idx+1)
        # The position within the block is:
        pos_in_block = k - cumulative_lengths[block_idx - 1] if block_idx > 0 else k
        
        # Now we need to find the digit at pos_in_block within the block consisting of 1, 2, ..., (block_idx+1)
        limit_num = block_idx + 1
        
        # Find which number in the sequence 1, 2, ..., limit_num contains the digit at pos_in_block
        current_pos = 1
        num = 1
        while True:
            s_num = str(num)
            num_len = len(s_num)
            
            if current_pos + num_len - 1 >= pos_in_block:
                # The digit is within this number
                digit_index_in_num = pos_in_block - current_pos
                # digit_index_in_num is 0-based index in the string representation of 'num'
                results.append(int(s_num[digit_index_in_num]))
                break
            else:
                current_pos += num_len
                num += 1

    for res in results:
        print(res)

if __name__ == "__main__":
    solve()