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

    queries = []
    for _ in range(q):
        n = int(next(iterator))
        k = int(next(iterator))
        queries.append((n, k))

    # Precompute lengths for n up to 10^5
    # f_0 length
    base_str = "What are you doing at the end of the world? Are you busy? Will you save us?"
    len_base = len(base_str)
    
    # Constants for the recursive structure
    # f_i = "What are you doing while sending " + f_{i-1} + "? Are you busy? Will you send " + f_{i-1} + "?"
    # Let A = "What are you doing while sending "
    # Let B = "? Are you busy? Will you send "
    # Let C = "?"
    # f_i = A + f_{i-1} + B + f_{i-1} + C
    
    A = "What are you doing while sending "
    B = "? Are you busy? Will you send "
    C = "?"
    
    len_A = len(A)
    len_B = len(B)
    len_C = len(C)
    
    # Precompute lengths
    # len_f[i] = len_A + len_f[i-1] + len_B + len_f[i-1] + len_C
    #          = len_A + len_B + len_C + 2 * len_f[i-1]
    #          = 26 + 2 * len_f[i-1] (since len_A+len_B+len_C = 26)
    # Wait, let's count:
    # A: "What are you doing while sending " -> 32 chars?
    # Let's recount carefully.
    # "What are you doing while sending "
    # W h a t (4) space (1) a r e (3) space (1) y o u (3) space (1) d o i n g (5) space (1) w h i l e (5) space (1) s e n d i n g (7) space (1)
    # 4+1+3+1+3+1+5+1+5+1+7+1 = 33?
    # Let's just use Python to count to be safe.
    
    # Actually, let's define the strings explicitly and count.
    A_str = "What are you doing while sending "
    B_str = "? Are you busy? Will you send "
    C_str = "?"
    
    len_A = len(A_str)
    len_B = len(B_str)
    len_C = len(C_str)
    
    # Calculate len_f for n up to 100000
    # Since k can be up to 10^18, we need to handle large n where length exceeds 10^18.
    # Once length >= 10^18, we can cap it at 10^18 + 7 (or just a value > max_k) to avoid overflow issues in logic,
    # but since we only care if k <= length, capping at max_k is sufficient.
    MAX_K = 10**18
    cap = MAX_K + 7
    
    lengths = [0] * 100001
    lengths[0] = len_base
    
    for i in range(1, 100001):
        prev_len = lengths[i-1]
        if prev_len >= cap:
            lengths[i] = cap
        else:
            new_len = len_A + prev_len + len_B + prev_len + len_C
            if new_len >= cap:
                lengths[i] = cap
            else:
                lengths[i] = new_len

    results = []
    
    for n, k in queries:
        if k > lengths[n]:
            results.append('.')
            continue
        
        # We need to find the k-th character (1-indexed)
        curr_n = n
        curr_k = k
        
        while curr_n > 0:
            # Structure: A + f_{curr_n-1} + B + f_{curr_n-1} + C
            # Lengths: len_A, lengths[curr_n-1], len_B, lengths[curr_n-1], len_C
            
            # Check if k falls in A
            if curr_k <= len_A:
                # Character is in A
                break
            
            curr_k -= len_A
            
            # Check if k falls in first f_{curr_n-1}
            prev_len = lengths[curr_n-1]
            if curr_k <= prev_len:
                # Character is in the first recursive part
                curr_n -= 1
                continue
            
            curr_k -= prev_len
            
            # Check if k falls in B
            if curr_k <= len_B:
                # Character is in B
                break
            
            curr_k -= len_B
            
            # Check if k falls in second f_{curr_n-1}
            if curr_k <= prev_len:
                # Character is in the second recursive part
                curr_n -= 1
                continue
            
            curr_k -= prev_len
            
            # Check if k falls in C
            if curr_k <= len_C:
                # Character is in C
                break
            
            # If we are here, k is out of bounds for this level, which shouldn't happen if initial check passed
            # But due to capping, it might. If curr_k is still > 0 and we are at base, we handle it.
            # However, if we capped, lengths[curr_n-1] might be cap, but actual length is huge.
            # If k was within actual length but we capped, we need to be careful.
            # But if k <= lengths[n] (actual or capped), and we subtract parts, we should land somewhere.
            # The only issue is if we capped, lengths[curr_n-1] is cap, but curr_k is small.
            # If curr_k <= cap, and we subtract len_A, len_B, etc., we might still be <= cap.
            # But if the real length was huge, and we are in the recursive part, we just go deeper.
            # The logic holds as long as we don't assume the exact length when it's capped, 
            # EXCEPT when we decide to stop and look up the character.
            # If we stop because curr_k <= len_A, len_B, or len_C, we are fine.
            # If we stop because we hit base case (curr_n == 0), we look up in base string.
            
            # If curr_k > prev_len (second part) and we haven't broken yet, it means k is in C or beyond.
            # We subtracted prev_len. Now curr_k is relative to C.
            # If curr_k <= len_C, break.
            # If curr_k > len_C, then k is beyond the string, which contradicts initial check unless capping messed up.
            # If capping happened, lengths[curr_n-1] = cap.
            # If real length was huge, and curr_k <= cap, we might think it's in the second part.
            # But if real length was huge, then k <= real length is true.
            # If we are in the second part, we recurse.
            # The only risk is if we think we are in the second part but actually k is in C?
            # No, because we check <= prev_len first.
            # If prev_len is capped (huge), and k is small, we enter the second part recursion.
            # This is correct because the second part is indeed huge and contains k.
            # So the logic is sound.
            
            # One edge case: if curr_k > len_C after subtracting everything, it means k is out of bounds.
            # But we checked k <= lengths[n] at the start.
            # If lengths[n] was capped, and k <= cap, it's possible k is actually out of bounds of the real string?
            # No, because if lengths[n] is capped, it means real length >= cap.
            # And k <= cap <= real length. So k is always valid if k <= lengths[n] (capped or not).
            
            # Wait, if lengths[n] is capped, it means real length >= cap.
            # If k <= cap, then k <= real length.
            # So k is always valid.
            
            # What if we are at the bottom and curr_n becomes 0?
            # Then we break out of loop and access base string.
            # But we need to ensure curr_k is valid for base string.
            # If we entered the loop with curr_n > 0, and we reduced curr_n to 0, it means we were in a recursive part.
            # Eventually we must hit a part that is not recursive (base) or a literal string (A, B, C).
            # If we hit base (curr_n=0), we check if curr_k <= len_base.
            # Since k was valid initially, and we only subtracted valid lengths, curr_k should be valid.
            # Unless we skipped a level where length was capped?
            # If length was capped, it means real length is huge.
            # If we are in that huge part, we recurse.
            # We will eventually hit a level where length is not capped (small n) or we hit a literal.
            # So it's fine.
            
            # However, there is a case: if we are at curr_n=0, we break the loop.
            # Then we need to access base_str[curr_k-1].
            # But we must ensure curr_k <= len_base.
            # If k was very large, and we were in a capped level, we might have recursed down to 0?
            # No, if we are in a capped level (n large), and k is small, we might go into A, B, C or the recursive parts.
            # If we go into recursive parts, we decrease n.
            # Eventually n becomes small enough that length is not capped, or we hit a literal.
            # If we hit n=0, it means we were in the base string's recursive expansion?
            # No, f_0 is base. f_1 uses f_0.
            # If we are at n=0, we are looking at f_0 directly.
            # If we reached n=0 via recursion, it means we were in a part of f_1, f_2... that maps to f_0.
            # And since k was valid, curr_k must be valid for f_0.
            
            # One detail: if we break because curr_k <= len_A, len_B, or len_C, we exit the loop.
            # Then we need to access the corresponding string.
            # If we break because of A, we access A_str.
            # If B, B_str.
            # If C, C_str.
            # If we exit because curr_n == 0, we access base_str.
            
            # But wait, the loop condition is `while curr_n > 0`.
            # If we break inside, we exit.
            # If we finish the loop (curr_n becomes 0), we exit.
            # So we need to handle both cases.
            
            # Let's restructure to make it clear.
            pass
        
        # After the loop, we have a state:
        # Either we broke out because we found a literal string (A, B, C)
        # Or we reduced curr_n to 0, meaning we are in f_0.
        
        # But wait, if we break inside, we need to know which string.
        # Let's refactor the loop to set a flag or variable.
        
        # Actually, let's just implement the logic cleanly inside the loop and break appropriately.
        # We can use a variable `found` and `source_str` and `index`.
        
        found = False
        source_str = ""
        idx = 0
        
        temp_n = n
        temp_k = k
        
        while temp_n > 0:
            # Check A
            if temp_k <= len_A:
                source_str = A_str
                idx = temp_k - 1
                found = True
                break
            
            temp_k -= len_A
            
            # Check first f_{temp_n-1}
            prev_len = lengths[temp_n-1]
            if temp_k <= prev_len:
                temp_n -= 1
                continue
            
            temp_k -= prev_len
            
            # Check B
            if temp_k <= len_B:
                source_str = B_str
                idx = temp_k - 1
                found = True
                break
            
            temp_k -= len_B
            
            # Check second f_{temp_n-1}
            if temp_k <= prev_len:
                temp_n -= 1
                continue
            
            temp_k -= prev_len
            
            # Check C
            if temp_k <= len_C:
                source_str = C_str
                idx = temp_k - 1
                found = True
                break
            
            # If we are here, temp_k > len_C, which implies k is out of bounds for this level.
            # But we checked k <= lengths[n] initially.
            # If lengths[n] was capped, and temp_k > len_C, it means we are in the second part?
            # No, we checked second part.
            # If temp_k > prev_len (second part), then we subtracted prev_len and are now in C.
            # If temp_k > len_C, then k is beyond C.
            # This means k is beyond the entire string f_{temp_n}.
            # But we checked k <= lengths[n] at the start.
            # If lengths[n] was capped, it means real length >= cap.
            # And k <= cap.
            # So k should be within bounds.
            # The only way temp_k > len_C is if we are in a situation where the string is longer than we think?
            # No, the structure is fixed.
            # If temp_k > len_C, it means k is beyond the string.
            # This should not happen if k <= lengths[n] (capped or not).
            # Unless... lengths[temp_n-1] was capped, but we are in the second part?
            # If lengths[temp_n-1] is capped, it means the recursive part is huge.
            # If temp_k <= prev_len (capped), we recurse.
            # If temp_k > prev_len, we go to C.
            # If temp_k > len_C, then k is beyond the string.
            # But if prev_len was capped, it means the recursive part is huge, so temp_k <= prev_len should be true for any reasonable k.
            # So we would have recursed.
            # So we only reach C if temp_k > prev_len.
            # If prev_len was capped, temp_k (which is <= cap) would be <= prev_len (cap).
            # So we would recurse.
            # So we only reach C if prev_len was NOT capped (or temp_k > actual prev_len).
            # If prev_len was not capped, then lengths[temp_n-1] is exact.
            # And if temp_k > prev_len, then k is beyond the second part.
            # Then we check C.
            # If temp_k > len_C, then k is beyond the whole string.
            # But we checked k <= lengths[n] at the start.
            # So this case should not happen.
            
            # Wait, what if lengths[n] was capped, but we are at a level where lengths[temp_n] is NOT capped?
            # Then lengths[n] >= lengths[temp_n] (since lengths is increasing).
            # If k <= lengths[n], it doesn't guarantee k <= lengths[temp_n].
            # Example: n=100 (capped), k=10^18.
            # lengths[100] = cap.
            # lengths[50] might be 10^18 (exact or capped).
            # If lengths[50] is exact and < k, then k > lengths[50].
            # But we are at n=100.
            # We subtract A, then check first f_99.
            # lengths[99] is likely capped.
            # So temp_k <= lengths[99] (capped) is true.
            # We recurse to n=99.
            # Eventually we reach a level where length is not capped?
            # Or we reach a level where we hit a literal.
            # If we reach a level where length is not capped, and k > length, then k is out of bounds.
            # But we know k <= lengths[n] (capped).
            # If lengths[n] is capped, real length >= cap.
            # If k <= cap, then k <= real length.
            # So k is always valid.
            # So we will never have temp_k > actual length at any level.
            # Because if we are at level m, and k <= lengths[n] (capped), and lengths[m] is exact.
            # If lengths[m] < k, then k > lengths[m].
            # But lengths[m] <= lengths[n] (since lengths is non-decreasing).
            # So k > lengths[n]. Contradiction.
            # So k <= lengths[m] for all m <= n.
            # So temp_k will always be <= actual length at any level we visit.
            # So we will never fall through to "k out of bounds".
            
            # So the logic is safe.
            pass
        
        if found:
            results.append(source_str[idx])
        else:
            # We reduced temp_n to 0
            # Now we are in f_0
            if temp_k <= len_base:
                results.append(base_str[temp_k-1])
            else:
                # Should not happen
                results.append('.')

    print("".join(results))

if __name__ == '__main__':
    solve()