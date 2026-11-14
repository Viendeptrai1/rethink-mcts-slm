import sys

def solve():
    # Base string
    base = "What are you doing at the end of the world? Are you busy? Will you save us?"
    len_base = len(base)
    
    # Constants for the structure of f_i for i >= 1
    prefix = "What are you doing while sending \""
    suffix = "\"? Are you busy? Will you send \""
    suffix_end = "\"?"
    
    # Lengths of the fixed parts
    len_prefix = len(prefix)
    len_suffix = len(suffix)
    len_suffix_end = len(suffix_end)
    
    # Precompute lengths of f_n
    # Since k <= 10^18, we only need to track lengths up to slightly more than 10^18.
    # Any length beyond that can be capped at 10^18 + 7 to avoid overflow and simplify logic.
    LIMIT = 10**18 + 7
    max_k = 10**18
    
    # We know that the length grows exponentially.
    # f_0 length is ~76
    # f_1 length = len_prefix + len(f_0) + len_suffix + len(f_0) + len_suffix_end
    #            = len_prefix + 2*len(f_0) + len_suffix + len_suffix_end
    # This growth is roughly doubling each time.
    # 2^60 is approx 10^18, so we only need about 60-70 iterations.
    
    lengths = [len_base]
    
    current_len = len_base
    i = 1
    while True:
        # Calculate length of f_i
        # f_i = prefix + f_{i-1} + suffix + f_{i-1} + suffix_end
        new_len = len_prefix + current_len + len_suffix + current_len + len_suffix_end
        if new_len > LIMIT:
            new_len = LIMIT
        lengths.append(new_len)
        current_len = new_len
        i += 1
        if i > 100: # Safety break, though loop will exit much earlier due to LIMIT
            break
            
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        q = int(next(iterator))
    except StopIteration:
        return
        
    results = []
    
    for _ in range(q):
        try:
            n = int(next(iterator))
            k = int(next(iterator))
        except StopIteration:
            break
            
        # If n is large enough such that length is capped at LIMIT, 
        # the effective length is LIMIT (or max_k if we want to be strict, but LIMIT > max_k).
        # However, the problem says if f_n has less than k characters, output '.'.
        # Since we capped at LIMIT, if k > actual_length, we output '.'.
        # But our capped length is > max_k (10^18), so if k <= 10^18, it's always within bounds for large n.
        # The only case we output '.' is if n is small and k is large.
        
        # Get the actual length for this n
        if n >= len(lengths):
            actual_len = LIMIT # Effectively infinite for our purposes
        else:
            actual_len = lengths[n]
            
        if k > actual_len:
            results.append('.')
            continue
            
        # Now find the k-th character (1-indexed)
        # We use a recursive approach with memoization or iterative descent.
        # Since n can be up to 10^5, but lengths stabilize quickly, we handle large n specially.
        
        # If n is very large, the structure is:
        # prefix + f_{n-1} + suffix + f_{n-1} + suffix_end
        # Since lengths[n-1] is capped at LIMIT, and k <= 10^18 < LIMIT,
        # we can just simulate the descent.
        
        # Optimization: if n is large (>= 60), the length of f_{n-1} is effectively LIMIT.
        # But we need to be careful. Let's just use the precomputed lengths array.
        # If n is larger than the array size, we treat length as LIMIT.
        
        curr_n = n
        curr_k = k
        
        while curr_n > 0:
            # Structure of f_{curr_n}:
            # Part 1: prefix (len_prefix)
            # Part 2: f_{curr_n-1} (lengths[curr_n-1])
            # Part 3: suffix (len_suffix)
            # Part 4: f_{curr_n-1} (lengths[curr_n-1])
            # Part 5: suffix_end (len_suffix_end)
            
            # Get length of f_{curr_n-1}
            if curr_n - 1 >= len(lengths):
                len_prev = LIMIT
            else:
                len_prev = lengths[curr_n - 1]
                
            # Check which part k falls into
            if curr_k <= len_prefix:
                # It's in the prefix
                curr_k -= len_prefix
                # We need the (curr_k)-th char of prefix
                # Adjust index to 0-based
                results.append(prefix[curr_k - 1])
                break
            else:
                curr_k -= len_prefix
                
            if curr_k <= len_prev:
                # It's in the first f_{curr_n-1}
                curr_n -= 1
                continue
            else:
                curr_k -= len_prev
                
            if curr_k <= len_suffix:
                # It's in the suffix
                results.append(suffix[curr_k - 1])
                break
            else:
                curr_k -= len_suffix
                
            if curr_k <= len_prev:
                # It's in the second f_{curr_n-1}
                curr_n -= 1
                continue
            else:
                curr_k -= len_prev
                
            # It's in suffix_end
            results.append(suffix_end[curr_k - 1])
            break
            
        else:
            # If loop finishes and curr_n == 0, we are in f_0
            # f_0 is the base string
            if curr_k <= len_base:
                results.append(base[curr_k - 1])
            else:
                # Should not happen if checks are correct
                results.append('.')

    print("".join(results))

if __name__ == "__main__":
    solve()