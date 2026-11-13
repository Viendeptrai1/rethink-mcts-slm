import sys
import bisect

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    q = int(next(iterator))
    
    # Precompute prefix sums of lengths of blocks up to a reasonable limit
    # Block i has length = length of string representation of numbers from 1 to i
    # We need to handle k up to 10^9.
    # Let's estimate how many blocks we need.
    # Length of block i approx i * log10(i). Sum of lengths grows roughly as integral x*log(x) dx ~ x^2/2 * log(x).
    # If sum ~ 10^9, then x^2/2 * log(x) ~ 10^9. 
    # If x = 200,000: x^2 = 4e10, log(x)~5.8, product/2 ~ 1.16e11 > 10^9.
    # If x = 100,000: x^2 = 1e10, log(x)~5, product/2 ~ 2.5e10 > 10^9.
    # If x = 50,000: x^2 = 2.5e9, log(x)~4.7, product/2 ~ 5.8e9 > 10^9.
    # If x = 30,000: x^2 = 9e8, log(x)~4.5, product/2 ~ 2e9 > 10^9.
    # If x = 25,000: x^2 = 6.25e8, log(x)~4.4, product/2 ~ 1.3e9 > 10^9.
    # If x = 20,000: x^2 = 4e8, log(x)~4.3, product/2 ~ 8.6e8 < 10^9.
    # So max block index is around 20,000 to 30,000. Let's precompute up to 30,000 to be safe and efficient.
    
    MAX_BLOCKS = 30000
    block_lengths = []
    current_total_len = 0
    
    # Helper to get length of string for 1..n
    # But we build block by block.
    # Block i is "123...i"
    
    # We can generate lengths incrementally.
    # However, generating strings for every number up to 30000 might be slightly slow if done naively in a tight loop inside Python?
    # Actually 30000 is small. Let's do it carefully.
    
    # Precompute lengths of numbers 1 to MAX_BLOCKS
    num_lens = []
    curr_val = 0
    for i in range(1, MAX_BLOCKS + 2):
        s = str(i)
        curr_val += len(s)
        num_lens.append(curr_val)
    
    # Now compute block lengths
    # Block i length = sum(len(str(j)) for j in 1..i) = num_lens[i-1]
    # Total length after M blocks = sum(block_lengths[0..M])
    
    prefix_block_total = []
    current_total = 0
    
    for i in range(1, MAX_BLOCKS + 1):
        # Length of block i is num_lens[i-1] (since num_lens is 0-indexed, index i-1 corresponds to i)
        blk_len = num_lens[i-1]
        current_total += blk_len
        prefix_block_total.append(current_total)
        
        if current_total >= 10**9:
            break
            
    # If k is larger than our precomputed total, we need to extend.
    # But based on estimation, 30000 blocks should cover 10^9.
    # Let's verify max value in prefix_block_total
    # If not enough, we will extend dynamically in the query phase or precompute more.
    # Given the constraints and nature of the problem, 30000 is likely sufficient. 
    # But to be absolutely safe against edge cases, let's check the last value.
    # If prefix_block_total[-1] < 10^9, we need more.
    
    # Re-evaluate: 
    # Sum of lengths of 1..i is roughly i * (log10(i)+1)/2 ? No.
    # Average length of number in 1..i is approx log10(i)/2? No.
    # Let's just trust the loop to break early if needed, but we need to cover up to 10^9.
    # Let's increase MAX_BLOCKS if necessary inside the logic or just set it high enough.
    # Let's set MAX_BLOCKS = 50000 to be very safe. 50000 iterations is trivial.
    
    # Let's restart precomputation with a larger buffer just in case.
    MAX_BLOCKS = 50000
    prefix_block_total = []
    current_total = 0
    num_lens = [0] * (MAX_BLOCKS + 1)
    curr_len = 0
    for i in range(1, MAX_BLOCKS + 1):
        s = str(i)
        curr_len += len(s)
        num_lens[i] = curr_len
        current_total += curr_len
        prefix_block_total.append(current_total)
        if current_total >= 10**9:
            break
            
    # If still not enough (unlikely with 50000), we could extend, but 50000 is plenty.
    # Max k is 10^9. 
    # With 50000 blocks, total length is huge.
    
    def find_digit(k):
        # Step 1: Find which block contains the k-th digit
        # Binary search on prefix_block_total
        idx = bisect.bisect_left(prefix_block_total, k)
        
        # If k is exactly equal to some prefix sum, it means the k-th digit is the last digit of the previous block?
        # Wait, bisect_left returns the first index where value >= k.
        # If prefix_block_total[idx] == k, then the k-th digit is the LAST digit of block (idx).
        # If prefix_block_total[idx-1] < k < prefix_block_total[idx], then it's inside block idx.
        
        if idx == 0:
            # This shouldn't happen since k >= 1 and prefix_block_total[0] >= 1
            return str(1)[0]
            
        if prefix_block_total[idx - 1] >= k:
            idx -= 1
            
        # Now idx is the 0-based index of the block in our list (which corresponds to block number idx+1)
        block_num = idx + 1
        
        # Calculate how many digits are BEFORE this block
        digits_before_block = 0
        if idx > 0:
            digits_before_block = prefix_block_total[idx - 1]
        
        offset = k - digits_before_block - 1 # 0-based offset within the block
        
        # The block contains numbers 1 to block_num concatenated.
        # We need to find which number in 1..block_num contains the offset-th digit.
        # And which digit of that number.
        
        # We can iterate or binary search over the numbers 1..block_num.
        # Since block_num is up to ~50000, linear scan might be too slow if we do it for every query (500 queries * 50000 = 2.5e7, acceptable in Python?).
        # But we can optimize by precomputing cumulative lengths of numbers.
        
        # Let's precompute cumulative lengths of numbers 1..N for N up to MAX_BLOCKS.
        # We already have num_lens, but we need cumulative sum of num_lens.
        # Let's create cum_num_lens where cum_num_lens[i] = total digits in numbers 1..i.
        # Actually num_lens[i] already stores sum of lengths 1..i.
        # Yes, num_lens[i] is exactly what we need.
        
        # We need to find smallest m such that num_lens[m] > offset.
        # The number is m.
        # The digit index within the number m is offset - num_lens[m-1].
        
        # Binary search on num_lens array for range 1..block_num
        # num_lens is 0-indexed but values are for 1..N at index N.
        # We search in range [1, block_num]
        
        low, high = 1, block_num
        target_num = -1
        
        while low <= high:
            mid = (low + high) // 2
            if num_lens[mid] <= offset:
                low = mid + 1
            else:
                target_num = mid
                high = mid - 1
        
        # target_num is the number containing the digit
        # Digit index within target_num
        prev_len = num_lens[target_num - 1] if target_num > 1 else 0
        digit_idx_in_num = offset - prev_len
        
        # Convert target_num to string and pick the digit
        s_num = str(target_num)
        return s_num[digit_idx_in_num]

    results = []
    for _ in range(q):
        k = int(next(iterator))
        results.append(find_digit(k))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()