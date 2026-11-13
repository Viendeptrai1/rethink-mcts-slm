import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    q = int(next(iterator))
    
    # Precompute block lengths and cumulative lengths
    # block[i] = length of the i-th block (1-indexed)
    # cum[i] = sum of lengths of blocks 1 to i
    # We need to go up to k = 10^9.
    # Let's estimate how many blocks we need.
    # Length of block i is roughly i * log10(i).
    # Sum of lengths up to N is roughly integral x log x dx ~ 0.5 * N^2 * log N.
    # If N = 10^5, N^2 = 10^10, too big.
    # If N = 10^4, N^2 = 10^8, times 0.5 * log(10^4) ~ 0.5 * 4 = 2 -> 2*10^8.
    # If N = 20000, N^2 = 4*10^8, times 0.5 * log(20000) ~ 0.5 * 4.3 = 2.15 -> ~8.6*10^8.
    # If N = 25000, N^2 = 6.25*10^8, times 0.5 * 4.4 = 2.2 -> ~1.375*10^9.
    # So N around 20000-25000 should cover 10^9.
    # Let's precompute up to 30000 to be safe.
    
    MAX_BLOCKS = 30000
    block_len = [0] * (MAX_BLOCKS + 1)
    cum_len = [0] * (MAX_BLOCKS + 1)
    
    # Helper to get length of string representation of x
    def get_len(x):
        return len(str(x))
    
    current_total = 0
    for i in range(1, MAX_BLOCKS + 1):
        # Length of block i is sum of lengths of numbers 1..i
        # We can compute this incrementally or just sum.
        # Since MAX_BLOCKS is 30000, summing inside loop is 30000^2 / 2 ~ 4.5*10^8 operations, too slow.
        # We need incremental update.
        # len_block[i] = len_block[i-1] + len(str(i))
        # But we need to be careful: block i contains 1, 2, ..., i.
        # block i-1 contains 1, 2, ..., i-1.
        # So len(block i) = len(block i-1) + len(str(i))
        
        l_i = get_len(i)
        if i == 1:
            block_len[i] = l_i
        else:
            block_len[i] = block_len[i-1] + l_i
        
        current_total += block_len[i]
        cum_len[i] = current_total
        
        if current_total >= 10**9:
            break
            
    # Process queries
    results = []
    for _ in range(q):
        k = int(next(iterator))
        
        # Find which block k falls into
        # Find largest i such that cum_len[i] < k
        # Then k is in block i+1
        # We can use binary search or linear scan since MAX_BLOCKS is small (30000)
        
        # Linear scan is fine for 30000 iterations per query? 500 * 30000 = 1.5*10^7, acceptable in Python.
        # But binary search is better.
        
        low = 1
        high = MAX_BLOCKS
        idx = -1
        
        while low <= high:
            mid = (low + high) // 2
            if cum_len[mid] < k:
                idx = mid
                low = mid + 1
            else:
                high = mid - 1
        
        # idx is the last block completely before k
        # So k is in block (idx + 1)
        if idx == -1:
            block_num = 1
        else:
            block_num = idx + 1
            
        # Position within the block (1-based)
        pos_in_block = k - cum_len[idx] if idx > 0 else k
        
        # Now we need to find the digit at pos_in_block in the sequence "123...block_num"
        # This is a standard problem: find the number containing the pos_in_block-th digit, then the digit.
        
        current_pos = 1
        num_len = 1
        start_num = 1
        
        while True:
            count_nums = 10 ** num_len - 10 ** (num_len - 1) if num_len > 1 else 9
            if num_len == 1:
                count_nums = 9
            else:
                # Numbers with num_len digits: 10^(num_len-1) to 10^num_len - 1
                # Count = 9 * 10^(num_len-1)
                count_nums = 9 * (10 ** (num_len - 1))
            
            # How many numbers of this length are left in our sequence up to block_num?
            # The sequence goes from 1 to block_num.
            # We are currently at start_num.
            # We need to see how many numbers of length 'num_len' are there from start_num to block_num.
            
            if start_num > block_num:
                # Should not happen if logic is correct
                break
            
            # Number of digits in current length group available
            if start_num > block_num:
                available = 0
            else:
                # Upper bound for this length group is min(block_num, 10^num_len - 1)
                upper = min(block_num, 10 ** num_len - 1)
                lower = 10 ** (num_len - 1)
                if lower > upper:
                    available = 0
                else:
                    available = upper - lower + 1
            
            if available == 0:
                num_len += 1
                start_num = 10 ** (num_len - 1)
                continue
            
            digits_available = available * num_len
            
            if current_pos + digits_available >= pos_in_block:
                # The target digit is within this length group
                # Find which number
                # We need to skip full numbers
                # (pos_in_block - 1) // num_len gives how many full numbers to skip
                # But we must ensure we don't skip past block_num
                
                # Actually, simpler:
                # We are at start_num. We have 'available' numbers.
                # We need to find the specific number.
                
                # Number of full numbers to skip
                skip = (pos_in_block - 1) // num_len
                # The number we want is start_num + skip
                target_num = start_num + skip
                
                # The digit index within target_num (0-based)
                digit_idx = (pos_in_block - 1) % num_len
                
                # Convert to string and get digit
                s = str(target_num)
                results.append(s[digit_idx])
                break
            else:
                current_pos += digits_available
                num_len += 1
                start_num = 10 ** (num_len - 1)

    for res in results:
        print(res)

if __name__ == '__main__':
    solve()