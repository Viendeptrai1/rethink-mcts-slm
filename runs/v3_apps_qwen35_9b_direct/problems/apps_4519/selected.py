import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    q = int(data[idx])
    idx += 1
    
    results = []
    
    for _ in range(q):
        n = int(data[idx])
        k = int(data[idx+1])
        s = data[idx+2]
        idx += 3
        
        # We will build the result character by character
        # We need to find the leftmost '0' that we can bring to the current position
        # within the remaining k moves.
        
        # Convert string to list for mutability if needed, but we'll build a new list
        res = [''] * n
        current_k = k
        current_pos = 0
        
        # We iterate through the original string to find the next '0' to place
        # However, a more efficient approach:
        # We maintain a pointer to the next available character in the original string
        # and try to bring the nearest '0' to the current position 'current_pos'.
        
        # Let's reframe:
        # We want to fill res[0], then res[1], etc.
        # For position i, we look for the first '0' in the remaining part of s (starting after the last used index)
        # such that the cost to move it to position i is <= current_k.
        # The cost is (index_of_0_in_original - i).
        # But wait, the indices shift as we move characters.
        # Actually, if we decide to move a '0' from original index `j` to current position `i`,
        # the number of swaps required is exactly `j - i` assuming all characters between `i` and `j` are already placed or skipped?
        # No, simpler logic:
        # We process the string from left to right. We maintain a pointer `next_idx` to the start of the unprocessed suffix of `s`.
        # For the current target position `pos` (starting at 0), we scan forward from `next_idx` to find the first '0'.
        # Let this '0' be at original index `j`.
        # The cost to bring this '0' to `pos` is `j - pos`.
        # If `j - pos <= current_k`, we can move it. We place '0' at `res[pos]`, decrement `k` by `j - pos`, and advance `next_idx` to `j + 1`.
        # If `j - pos > current_k`, we cannot bring this '0' to `pos`. Since this is the first '0' available, we cannot bring any subsequent '0' either (they are even further).
        # So we must place the character at `s[next_idx]` (which must be '1' in this case, because if it were '0' we would have picked it) at `res[pos]`.
        # Then we move to `pos + 1` and `next_idx + 1`.
        
        # Wait, the logic above has a flaw: if we skip a '0' because it's too far, we might be able to bring a later '0'?
        # No, because later '0's are at even larger indices, so the cost `j' - pos` would be even larger.
        # So the greedy strategy works: always try to bring the nearest available '0'.
        # If we can't, we are forced to take the nearest available '1' (which is the current head of the unprocessed string).
        
        # Refined Algorithm:
        # 1. Convert s to a list of characters or just use string indexing.
        # 2. Initialize `res` as a list of size n.
        # 3. `next_idx` = 0 (points to the first unprocessed character in s)
        # 4. `pos` = 0 (current position we are filling in res)
        # 5. While `pos` < n:
        #    a. Find the first '0' in s starting from `next_idx`. Let its index be `zero_idx`.
        #       If no '0' exists from `next_idx` to end, then all remaining are '1's.
        #    b. If a '0' exists:
        #       cost = `zero_idx` - `pos`
        #       If `cost <= current_k`:
        #           res[pos] = '0'
        #           current_k -= cost
        #           next_idx = zero_idx + 1
        #           pos += 1
        #       Else:
        #           # Cannot bring this '0'. Must take the current head (which is '1')
        #           res[pos] = s[next_idx]
        #           next_idx += 1
        #           pos += 1
        #    c. If no '0' exists (or we chose to skip because cost > k, but actually if cost > k we just take the '1'):
        #       Wait, if cost > k, we take s[next_idx]. What is s[next_idx]?
        #       If there is a '0' later, s[next_idx] is '1'.
        #       If there is no '0' later, s[next_idx] is '1'.
        #       So in both cases where we don't move a '0', we just take s[next_idx] and advance.
        #       BUT, we need to be careful. If we take s[next_idx] and it is '1', we just output '1'.
        #       The only decision is: can we bring the nearest '0'?
        
        # Optimization: Scanning for '0' every time might be O(N^2) in worst case (e.g., 111...100...0).
        # We need O(N).
        # We can precompute the positions of all '0's.
        
        zero_positions = [i for i, c in enumerate(s) if c == '0']
        zero_ptr = 0 # Pointer to the next zero in zero_positions
        
        res = []
        current_k = k
        pos = 0
        next_idx = 0
        
        while pos < n:
            # Check if there is a zero available
            if zero_ptr < len(zero_positions):
                zero_idx = zero_positions[zero_ptr]
                # Is this zero still in the unprocessed part?
                # Since we process left to right, and we only advance next_idx,
                # we must ensure zero_idx >= next_idx.
                # Actually, zero_positions are sorted. If zero_ptr points to a zero that is before next_idx,
                # it means we already processed it? No, we skip characters.
                # If we skipped a character, it was a '1'. So any zero before next_idx would have been skipped?
                # No, if we skipped a character, it means we took it as is.
                # If we took a '1' at `next_idx`, then `next_idx` increments.
                # If `zero_idx` < `next_idx`, it means this zero was already passed over?
                # But we only pass over characters if we decide to take them as '1's.
                # If we encounter a '0' at `zero_idx` and `zero_idx == next_idx`, we consider moving it.
                # If `zero_idx > next_idx`, it means there are some '1's between `next_idx` and `zero_idx`.
                # We haven't processed those '1's yet.
                # So the condition is simply: is `zero_idx >= next_idx`?
                # Yes. And since we iterate `pos` from 0, and `next_idx` starts at 0,
                # and `zero_idx` is increasing, we just need to check if `zero_ptr` is valid and `zero_positions[zero_ptr] >= next_idx`.
                # Actually, since we only increment `next_idx` when we consume a character,
                # and `zero_positions` contains indices of all zeros,
                # if `zero_ptr` points to a zero that is < `next_idx`, it means we already consumed it?
                # No, if we consumed a character at `next_idx`, we incremented `next_idx`.
                # If that character was a '0', we would have moved it (if k allowed) or... wait.
                # If the character at `next_idx` is '0', then `zero_positions[zero_ptr]` must be `next_idx`.
                # So `zero_idx` will always be >= `next_idx` if `zero_ptr` is valid and we haven't skipped it.
                # But what if we skipped a '0'? We never skip a '0' unless we can't move it.
                # If we can't move it (cost > k), we take the current head.
                # If the current head is '0', then cost = 0, so we always move it.
                # So we never skip a '0' that is at `next_idx`.
                # Therefore, `zero_positions[zero_ptr]` will always be >= `next_idx` as long as `zero_ptr` is valid.
                
                cost = zero_idx - pos
                if cost <= current_k:
                    res.append('0')
                    current_k -= cost
                    zero_ptr += 1
                    next_idx = zero_idx + 1 # Skip this zero
                    pos += 1
                else:
                    # Cannot bring this zero. Must take the current head.
                    # The current head is s[next_idx]. Since we can't bring the zero at zero_idx,
                    # and zero_idx > next_idx (because if zero_idx == next_idx, cost = zero_idx - pos.
                    # If zero_idx == next_idx, then cost = next_idx - pos.
                    # If next_idx == pos, cost = 0 <= k. So we would have taken it.
                    # So if we are here, cost > k, which implies next_idx > pos.
                    # Thus s[next_idx] must be '1' (because if it were '0', it would be the zero at zero_ptr).
                    res.append(s[next_idx])
                    next_idx += 1
                    pos += 1
            else:
                # No more zeros, all remaining are '1's
                res.append(s[next_idx])
                next_idx += 1
                pos += 1
        
        results.append("".join(res))
    
    print("\n".join(results))

if __name__ == '__main__':
    solve()