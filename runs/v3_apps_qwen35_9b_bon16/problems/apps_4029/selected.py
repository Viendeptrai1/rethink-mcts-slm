import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    n = len(s)
    
    # Target suffixes for divisibility by 25: "00", "25", "50", "75"
    targets = ["00", "25", "50", "75"]
    
    min_moves = float('inf')
    
    for t in targets:
        c1, c2 = t[0], t[1]
        idx1 = -1
        idx2 = -1
        
        # Find first occurrence of c1
        for i in range(n):
            if s[i] == c1:
                idx1 = i
                break
        
        if idx1 == -1:
            continue
            
        # Find first occurrence of c2 after idx1
        idx2 = -1
        for i in range(idx1 + 1, n):
            if s[i] == c2:
                idx2 = i
                break
        
        if idx2 == -1:
            continue
            
        # Calculate moves to bring c2 to position n-1 and c1 to n-2
        # Original positions: idx1, idx2
        # Target positions: n-2, n-1
        
        # Moves to move c2 to n-1
        moves = (n - 1) - idx2
        
        # Moves to move c1 to n-2
        # If c1 was to the right of the original position of c2, it shifts left by 1 because c2 moved left past it
        if idx1 > idx2:
            moves += (n - 2) - idx1
        else:
            moves += (n - 2) - idx1
            
        # Check for leading zero constraint
        # After moving, the first digit cannot be '0'.
        # We need to determine what the new first digit is.
        # The digits at indices 0 to min(idx1, idx2)-1 are untouched relative to each other,
        # but their absolute indices might shift if one of the chosen digits was at index 0.
        
        # Let's simulate the final string construction to check leading zero efficiently
        # We construct the final string by taking the original string, removing the two used digits,
        # and appending them at the end.
        
        chars = list(s)
        # Remove c2 at idx2
        chars.pop(idx2)
        # Remove c1 at idx1 (idx1 might have changed if idx1 > idx2)
        chars.pop(idx1 - 1 if idx1 > idx2 else idx1)
        
        # Append target
        chars.append(c2)
        chars.append(c1)
        
        final_s = "".join(chars)
        
        if final_s[0] == '0':
            continue
            
        if moves < min_moves:
            min_moves = moves
            
    if min_moves == float('inf'):
        print("-1")
    else:
        print(min_moves)

if __name__ == "__main__":
    solve()