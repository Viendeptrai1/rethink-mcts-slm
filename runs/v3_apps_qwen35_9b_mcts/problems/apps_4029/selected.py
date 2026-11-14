import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    n = len(s)
    
    # Check if already divisible by 25
    if int(s[-2:]) % 25 == 0:
        print(0)
        return
    
    # Target suffixes
    targets = ['00', '25', '50', '75']
    
    min_moves = float('inf')
    
    for t in targets:
        d1 = t[0]
        d2 = t[1]
        
        # Find all indices for d1 and d2
        idx1 = [i for i, c in enumerate(s) if c == d1]
        idx2 = [i for i, c in enumerate(s) if c == d2]
        
        if not idx1 or not idx2:
            continue
            
        # Try all combinations of one instance of d1 and one instance of d2
        for i in idx1:
            for j in idx2:
                if i == j:
                    continue
                
                # We need to move d1 to position n-2 and d2 to position n-1
                # Calculate cost based on relative order
                cost = 0
                if i < j:
                    # d1 is to the left of d2
                    # Move d1 to n-2: cost is (n-2 - i)
                    # Then move d2 to n-1: cost is (n-1 - j) because d1 moved left of d2? 
                    # Actually, if we move d1 first to n-2, d2 shifts left by 1 if d2 was after d1.
                    # But simpler: 
                    # Cost to bring d1 to n-2: (n-2 - i)
                    # After moving d1, d2 is at j-1 (if j > i) or j (if j < i)
                    # Then cost to bring d2 to n-1: (n-1 - new_j)
                    
                    # Let's do it logically:
                    # If i < j:
                    #   Move d1 from i to n-2. Swaps = (n-2) - i.
                    #   d2 was at j. Since j > i, d2 shifts to j-1.
                    #   Move d2 from j-1 to n-1. Swaps = (n-1) - (j-1) = n - j.
                    #   Total = (n-2-i) + (n-j) = 2n - 2 - i - j
                    cost = (n - 2 - i) + (n - 1 - (j - 1))
                else: # j < i
                    # d2 is to the left of d1
                    # Move d2 from j to n-1. Swaps = (n-1) - j.
                    # d1 was at i. Since i > j, d1 shifts to i-1.
                    # Move d1 from i-1 to n-2. Swaps = (n-2) - (i-1) = n - 1 - i.
                    # Total = (n-1-j) + (n-2-i) = 2n - 3 - i - j
                    cost = (n - 1 - j) + (n - 2 - (i - 1))
                
                # Check leading zero constraint
                # We are removing digits at i and j and placing them at the end.
                # The new first digit will be the first digit of the remaining string.
                # If the original string had length > 1, we just need to ensure that after removing i and j,
                # the first character is not '0'.
                # Special case: if n=2, after moving, the number is just the two digits. 
                # But the problem says "resulting number will not contain leading zeroes".
                # If the resulting number is "05" or "00", that's invalid.
                # However, our targets are 00, 25, 50, 75.
                # 00 is invalid as a number (leading zero unless it's just 0, but n>=1 and no leading zeros initially).
                # Wait, if n=2 and we form "00", is that allowed? 
                # "resulting number will not contain leading zeroes". 
                # Usually "00" is considered to have a leading zero. The number 0 is written as "0".
                # Since input has no leading zeros and n>=1, if result is "00", it's invalid.
                # If result is "25", "50", "75", they are fine.
                # If result is "00", it's invalid.
                # Also if n > 2, the first digit must not be '0'.
                
                # Construct the remaining sequence to check the first digit
                # We remove indices i and j from the original list of indices [0, 1, ..., n-1]
                # But we need to know which digit ends up at index 0.
                # The digits at indices 0 to n-1 excluding i and j form the prefix.
                # The first digit of the prefix is the one at the smallest index k in [0, n-1] such that k != i and k != j.
                
                first_digit_idx = -1
                for k in range(n):
                    if k != i and k != j:
                        first_digit_idx = k
                        break
                
                if first_digit_idx == -1:
                    # This happens if n=2 and we picked both digits.
                    # Then the number is just the two digits we moved.
                    # If target is "00", then the number is "00" -> invalid.
                    # If target is "25", "50", "75", then valid.
                    if t == '00':
                        continue
                    else:
                        # Valid, but we must ensure the number doesn't start with 0.
                        # Since t is not 00, the first digit is t[0] which is 2, 5, or 7. Not 0.
                        # So it's valid.
                        pass
                else:
                    if s[first_digit_idx] == '0':
                        continue
                
                if cost < min_moves:
                    min_moves = cost
    
    if min_moves == float('inf'):
        print(-1)
    else:
        print(min_moves)

if __name__ == '__main__':
    solve()