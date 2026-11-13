import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        q = int(next(iterator))
    except StopIteration:
        return

    results = []

    # Constants
    S0 = "What are you doing at the end of the world? Are you busy? Will you save us?"
    # Length of S0
    L0 = len(S0)
    
    # Fixed parts
    Prefix = "What are you doing while sending \""
    Suffix = "\"? Are you busy? Will you send \""
    End = "\"?"
    
    # Lengths of fixed parts
    len_prefix = len(Prefix)
    len_suffix = len(Suffix)
    len_end = len(End)
    
    # Total length of f_1 = len_prefix + len(S0) + len_suffix + len(S0) + len_end
    # Total length of f_i for i>=1: len_prefix + len(S_{i-1}) + len_suffix + len(S_{i-1}) + len_end
    # So len(f_i) = len_prefix + 2*len(f_{i-1}) + len_suffix + len_end
    
    # We need to compute lengths for n up to 10^5. Since k can be up to 10^18, lengths will exceed 10^18 quickly.
    # We can cap the lengths at 10^18 + 7 (or just 10^18 + some buffer) because if k <= 10^18, 
    # any length >= 10^18 is effectively infinity for our purposes.
    INF = 10**18 + 7
    
    # Precompute lengths
    lengths = [0] * (100001)
    lengths[0] = L0
    
    current_len = L0
    for i in range(1, 100001):
        # len_i = len_prefix + 2 * len_{i-1} + len_suffix + len_end
        val = len_prefix + 2 * current_len + len_suffix + len_end
        if val >= INF:
            current_len = INF
        else:
            current_len = val
        lengths[i] = current_len

    for _ in range(q):
        n = int(next(iterator))
        k = int(next(iterator))
        
        if n == 0:
            if k > lengths[0]:
                results.append('.')
            else:
                results.append(S0[k-1])
            continue
        
        if lengths[n] < k:
            results.append('.')
            continue
        
        # We need to find the k-th character of f_n
        curr = n
        target = k
        
        while True:
            if curr == 0:
                if target <= lengths[0]:
                    results.append(S0[target-1])
                else:
                    results.append('.')
                break
            
            # Structure of f_curr:
            # Part 1: Prefix (len_prefix)
            # Part 2: f_{curr-1} (lengths[curr-1])
            # Part 3: Suffix (len_suffix)
            # Part 4: f_{curr-1} (lengths[curr-1])
            # Part 5: End (len_end)
            
            l1 = len_prefix
            l2 = lengths[curr-1]
            l3 = len_suffix
            l4 = lengths[curr-1]
            l5 = len_end
            
            # Optimization: if l2 is capped at INF, we treat it as huge, but we need exact logic if target falls in it.
            # However, since we capped at INF, if target is within the capped range but the real length was huge,
            # our logic holds because we only care if target <= real_length. Since real_length >= INF >= target (if target <= 10^18),
            # the condition target <= l2 is true if we used capped values, UNLESS the real length was actually smaller than INF but we capped it.
            # But we only cap if it's >= INF. So if l2 is stored as INF, real length is >= INF.
            # If target <= 10^18, and real length >= INF, then target is definitely within bounds.
            
            if target <= l1:
                results.append(Prefix[target-1])
                break
            target -= l1
            
            if target <= l2:
                curr -= 1
                continue
            
            target -= l2
            
            if target <= l3:
                results.append(Suffix[target-1])
                break
            target -= l3
            
            if target <= l4:
                curr -= 1
                continue
            
            target -= l4
            
            if target <= l5:
                results.append(End[target-1])
                break
            target -= l5
            
            curr -= 1

    sys.stdout.write("".join(results) + "\n")

if __name__ == "__main__":
    solve()