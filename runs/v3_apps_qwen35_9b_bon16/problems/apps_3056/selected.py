import sys

def solve():
    s = sys.stdin.read().strip()
    if not s:
        return

    # We need to compute the sum of values of all walks matching the pattern.
    # Let n be the length of the pattern.
    # Each step can be L, R, or P.
    # Let's denote:
    #   count[i] = number of partial walks of length i that end at a node with value v? 
    # But the value depends on the path, not just the length.
    #
    # Alternative approach:
    # The value of a walk is determined by the sequence of moves.
    # Root is 1.
    # If current node is X:
    #   L -> 2X
    #   R -> 2X+1
    #   P -> X
    #
    # We can compute the expected contribution of each position independently using linearity of expectation (or summation).
    # However, the operations are multiplicative in nature (doubling).
    #
    # Let's consider the structure:
    # Value = 1 * (product of factors from moves) + (sum of additive parts)
    # Actually, let's expand the value formula.
    # Suppose the walk has length n.
    # Let the moves be m_1, m_2, ..., m_n.
    # If m_i is L: factor 2, add 0? No.
    # If m_i is R: factor 2, add 1?
    # If m_i is P: factor 1, add 0?
    #
    # Let's trace:
    # Start: 1
    # After m1:
    #   L: 2*1 = 2
    #   R: 2*1+1 = 3
    #   P: 1
    #
    # Notice that any node value can be written as:
    #   V = 1 * (2^k) + (some offset)
    # Actually, let's look at the binary representation or simply the recurrence.
    # V_{i} = 2 * V_{i-1} + (1 if R else 0) if not P.
    # If P, V_i = V_{i-1}.
    #
    # This looks like:
    # V = ( ... ( (1 * f1 + c1) * f2 + c2 ) ... ) fn + cn
    # where fi is 2 (if L/R) or 1 (if P)
    # and ci is 0 (if L/P) or 1 (if R)
    #
    # We can rewrite V as:
    # V = 1 * (f1 * f2 * ... * fn) 
    #   + c1 * (f2 * ... * fn)
    #   + c2 * (f3 * ... * fn)
    #   + ...
    #   + cn
    #
    # So, Sum(V) over all walks = 
    #   Sum_over_walks [ 1 * (prod f_i) + Sum_j (c_j * prod_{k=j+1}^n f_k) ]
    # = (Sum_over_walks [ prod f_i ]) + Sum_j [ (Sum_over_walks [ c_j * prod_{k=j+1}^n f_k] ) ]
    #
    # Let's define for each position i (0-indexed):
    #   Let A_i be the set of values of the prefix of length i (moves 0 to i-1).
    #   But we don't need the values, we need the sum of products of future multipliers.
    #
    # Let's reverse the thinking.
    # Let n = len(s).
    # For a specific position i (0 to n-1):
    #   The term corresponding to the base 1 is multiplied by the product of multipliers from i to n-1.
    #   The term corresponding to c_i (which is 1 if R, 0 otherwise) is multiplied by the product of multipliers from i+1 to n-1.
    #
    # Let P(i) be the sum of (product of multipliers from i to n-1) over all completions of the suffix s[i:].
    # Let C(i) be the sum of (product of multipliers from i+1 to n-1) over all completions, but only counting the cases where s[i] forces an addition.
    # Actually, let's break it down by position.
    #
    # Total Sum = Sum_{walk w} Value(w)
    # Value(w) = 1 * (f_0 * f_1 * ... * f_{n-1}) + 
    #            (1 if w[0]=='R' else 0) * (f_1 * ... * f_{n-1}) +
    #            (1 if w[1]=='R' else 0) * (f_2 * ... * f_{n-1}) +
    #            ...
    #            (1 if w[n-1]=='R' else 0)
    #
    # So Total Sum = 
    #   (Sum_{w} Product_{j=0}^{n-1} f_j(w)) +
    #   Sum_{i=0}^{n-1} [ (Sum_{w} I(w[i]=='R') * Product_{j=i+1}^{n-1} f_j(w) ) ]
    #
    # Note that f_j is 2 if w[j] in {L, R}, 1 if w[j] == 'P'.
    # I(w[i]=='R') is 1 if w[i] is 'R', else 0.
    #
    # Let's compute two things for each split point k (from 0 to n):
    # 1. The number of ways to complete the suffix starting at k, and the sum of products of multipliers for the suffix.
    #    Actually, we need:
    #    S_suffix[k] = Sum_{all completions w of s[k:]} (Product_{j=k}^{n-1} f_j(w))
    #    This is a single number.
    #
    # 2. For the "R" term at position i:
    #    We need Sum_{w} [ I(w[i]=='R') * Product_{j=i+1}^{n-1} f_j(w) ]
    #    This can be split into:
    #      (Number of ways to complete s[i+1:]) * (Sum over prefixes ending at i where w[i]=='R' of 1) * (S_suffix[i+1])
    #    Wait, the prefix part (0 to i-1) doesn't affect the multiplier product from i+1 onwards.
    #    The multiplier product from i+1 onwards only depends on the choices from i+1 to n-1.
    #    The condition w[i]=='R' fixes the choice at i.
    #    The choices before i don't affect the value of the product from i+1 onwards.
    #    So, for a fixed i:
    #      Term_i = (Count of ways to form prefix 0..i-1 matching s[0:i]) * 
    #               (1 if s[i] can be 'R') * 
    #               (Sum of products for suffix i+1..n-1)
    #               * (1 if s[i] is 'R') -> actually if s[i] is '*', we sum over 'R'. If 'R', we take 'R'. If 'L' or 'P', we take 0.
    #
    # Let's formalize:
    # Let N[k] = number of ways to complete the suffix s[k:] (i.e., match s[k:] with any valid walk suffix).
    # Let P[k] = sum of (product of multipliers from k to n-1) over all completions of s[k:].
    #
    # Base case: k = n.
    #   Suffix is empty. Product is 1 (empty product). Number of ways is 1.
    #   N[n] = 1
    #   P[n] = 1
    #
    # Recursive step for k from n-1 down to 0:
    #   char c = s[k]
    #   Possible moves M = []
    #   If c == 'L': M = ['L']
    #   If c == 'R': M = ['R']
    #   If c == 'P': M = ['P']
    #   If c == '*': M = ['L', 'R', 'P']
    #
    #   N[k] = sum( N[k+1] for m in M ) = |M| * N[k+1]
    #
    #   For P[k]:
    #     P[k] = sum_{m in M} ( multiplier(m) * P[k+1] )
    #     multiplier('L') = 2
    #     multiplier('R') = 2
    #     multiplier('P') = 1
    #     So, P[k] = P[k+1] * ( sum_{m in M} multiplier(m) )
    #
    # Now, let's compute the total sum.
    # Total Sum = (Sum_{w} Product_{j=0}^{n-1} f_j) + Sum_{i=0}^{n-1} ( Term_R_i )
    #
    # First part: Sum_{w} Product_{j=0}^{n-1} f_j
    #   This is exactly P[0]. Because P[0] sums over all walks the product of multipliers from 0 to n-1.
    #
    # Second part: Sum_{i=0}^{n-1} ( Term_R_i )
    #   Term_R_i = (Number of ways to match s[0:i]) * (Indicator that s[i] allows 'R') * (Sum of products for suffix i+1)
    #   Let Pre[i] = Number of ways to match prefix s[0:i].
    #   Then Term_R_i = Pre[i] * (1 if s[i] allows 'R' else 0) * P[i+1]
    #
    # We can compute Pre[i] iteratively.
    # Pre[0] = 1
    # Pre[i+1] = Pre[i] * |M_i|, where M_i is the set of allowed moves at s[i].
    #
    # Algorithm:
    # 1. Compute P array from n-1 down to 0.
    #    P[n] = 1
    #    For k in n-1..0:
    #      count_moves = 0
    #      sum_mult = 0
    #      for m in allowed(s[k]):
    #         count_moves += 1
    #         sum_mult += (2 if m in 'LR' else 1)
    #      N[k] = count_moves * N[k+1] (actually we don't need N explicitly for P, but good to know)
    #      P[k] = sum_mult * P[k+1]
    #
    # 2. Compute Pre array and accumulate the answer.
    #    ans = P[0]
    #    Pre[0] = 1 (conceptually, ways to match empty prefix)
    #    For i in 0..n-1:
    #       moves = allowed(s[i])
    #       count = len(moves)
    #       # Check if 'R' is in moves
    #       is_r = 1 if 'R' in moves else 0
    #       # Add contribution of R at position i
    #       ans += Pre[i] * is_r * P[i+1]
    #       
    #       # Update Pre for next step
    #       Pre[i+1] = Pre[i] * count
    #
    # Wait, let's re-verify the first part.
    # Value(w) = 1 * (prod f) + sum (c_j * prod_{k=j+1} f)
    # Sum(Value) = Sum(prod f) + Sum_j Sum_w (I(w[j]=='R') * prod_{k=j+1} f)
    # Sum(prod f) over all w is exactly P[0].
    # The second term: for a fixed j, we sum over all w.
    # w = prefix (0..j-1) + char_at_j + suffix (j+1..n-1)
    # The term is I(char_at_j == 'R') * (product of suffix multipliers).
    # The product of suffix multipliers depends only on the suffix.
    # The sum over all w factors into:
    #   (Sum over prefixes) * (Sum over char_at_j) * (Sum over suffixes of prod_suffix)
    # Sum over prefixes = Pre[j] (number of ways to match s[0:j])
    # Sum over char_at_j = 1 if 'R' is allowed at s[j], else 0. (Since if allowed, we pick 'R' once for the indicator to be 1, and there are no other contributions from this slot for this specific term).
    # Sum over suffixes of prod_suffix = P[j+1]
    # So yes, Term_j = Pre[j] * (1 if 'R' in allowed(s[j]) else 0) * P[j+1].
    #
    # One detail: Pre[j] is the number of ways to match s[0:j].
    # Pre[0] = 1.
    # Pre[1] = Pre[0] * |allowed(s[0])|
    # ...
    # Pre[i+1] = Pre[i] * |allowed(s[i])|
    #
    # Implementation details:
    # Allowed moves:
    #   'L' -> ['L']
    #   'R' -> ['R']
    #   'P' -> ['P']
    #   '*' -> ['L', 'R', 'P']
    #
    # Multipliers:
    #   'L', 'R' -> 2
    #   'P' -> 1
    #
    # Constraints: len(s) <= 10000.
    # The numbers can be very large. Python handles large integers automatically.
    # Complexity: O(n).

def solve():
    s = sys.stdin.read().strip()
    if not s:
        return

    n = len(s)
    
    # P[k] stores the sum of products of multipliers for all completions of suffix s[k:]
    # P[n] = 1
    P = [0] * (n + 1)
    P[n] = 1
    
    # Compute P backwards
    for k in range(n - 1, -1, -1):
        char = s[k]
        count_moves = 0
        sum_mult = 0
        
        if char == 'L':
            moves = ['L']
        elif char == 'R':
            moves = ['R']
        elif char == 'P':
            moves = ['P']
        else: # '*'
            moves = ['L', 'R', 'P']
        
        count_moves = len(moves)
        for m in moves:
            mult = 2 if m in 'LR' else 1
            sum_mult += mult
            
        P[k] = sum_mult * P[k+1]
        
    # Calculate total sum
    # Part 1: P[0]
    total_sum = P[0]
    
    # Pre[i] is the number of ways to match the prefix s[0:i]
    # Pre[0] = 1
    pre = 1
    
    for i in range(n):
        char = s[i]
        moves = []
        if char == 'L':
            moves = ['L']
        elif char == 'R':
            moves = ['R']
        elif char == 'P':
            moves = ['P']
        else:
            moves = ['L', 'R', 'P']
        
        is_r = 1 if 'R' in moves else 0
        count = len(moves)
        
        # Add contribution of 'R' at position i
        if is_r:
            total_sum += pre * P[i+1]
        
        # Update pre for next iteration
        pre *= count
        
    print(total_sum)

if __name__ == '__main__':
    solve()