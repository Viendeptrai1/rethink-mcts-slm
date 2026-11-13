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
    
    # Iterate over all possible lengths of the tandem repeat (must be even)
    # Let the tandem repeat length be 2 * period
    # The period can range from 1 to total_len // 2
    for period in range(1, total_len // 2 + 1):
        length = 2 * period
        # Check all possible starting positions for a tandem repeat of this length
        for start in range(total_len - length + 1):
            # Check if the substring s[start : start + length] is a valid tandem repeat
            # A tandem repeat of length 2*period means s[i] == s[i + period] for i in [start, start + period - 1]
            is_valid = True
            for i in range(period):
                idx1 = start + i
                idx2 = start + i + period
                
                # Check bounds for both characters
                if idx1 >= total_len or idx2 >= total_len:
                    is_valid = False
                    break
                
                char1 = s[idx1] if idx1 < n else None
                char2 = s[idx2] if idx2 < n else None
                
                if char1 is None or char2 is None:
                    is_valid = False
                    break
                
                if char1 != char2:
                    is_valid = False
                    break
            
            if is_valid:
                if length > max_l:
                    max_l = length
    
    print(max_l)

if __name__ == "__main__":
    solve()