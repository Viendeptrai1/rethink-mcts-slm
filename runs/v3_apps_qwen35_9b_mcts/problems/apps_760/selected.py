import sys

def solve():
    s = sys.stdin.readline().strip()
    k_line = sys.stdin.readline().strip()
    if not k_line:
        return
    k = int(k_line)
    
    n = len(s)
    total_len = n + k
    
    max_l = 0
    
    # Iterate over all possible starting positions i in the new string (0 to total_len-1)
    # and all possible half-lengths h such that the tandem repeat fits in total_len.
    # A tandem repeat of length 2*h starting at i requires indices i to i+2*h-1.
    # So i + 2*h <= total_len.
    
    for i in range(total_len):
        # Maximum possible half-length for this start position
        max_h = (total_len - i) // 2
        for h in range(1, max_h + 1):
            # Check if a tandem repeat of half-length h starting at i is possible
            possible = True
            for offset in range(h):
                idx1 = i + offset
                idx2 = i + h + offset
                
                # If either index is out of bounds of the new string, this h is too big (shouldn't happen due to loop limit)
                if idx2 >= total_len:
                    possible = False
                    break
                
                char1 = s[idx1] if idx1 < n else '?'
                char2 = s[idx2] if idx2 < n else '?'
                
                if char1 == '?' and char2 == '?':
                    # Both are in the added part, we can choose them to be equal
                    continue
                elif char1 == '?' or char2 == '?':
                    # One is in s, one is in added part. We can choose the added part char to match s.
                    continue
                else:
                    # Both are in s. They must be equal.
                    if char1 != char2:
                        possible = False
                        break
            
            if possible:
                current_l = 2 * h
                if current_l > max_l:
                    max_l = current_l
    
    print(max_l)

if __name__ == "__main__":
    solve()