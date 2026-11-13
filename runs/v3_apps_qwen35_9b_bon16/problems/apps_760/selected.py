import sys

def solve():
    s = sys.stdin.readline().strip()
    line2 = sys.stdin.readline().strip()
    if not line2:
        k = 0
    else:
        k = int(line2)

    n = len(s)
    total_len = n + k

    max_l = 0

    # We try all possible lengths l. Since l must be even (2*n), we can iterate n from 1 upwards.
    # The maximum possible n is total_len // 2.
    max_n = total_len // 2

    for n_len in range(1, max_n + 1):
        l = 2 * n_len
        # The tandem repeat has length l, so it starts at some index i and ends at i + l - 1.
        # The start index i can range from 0 to total_len - l.
        for i in range(total_len - l + 1):
            # Check if a tandem repeat of length l can start at i
            # It consists of two halves: first half [i, i+n_len-1], second half [i+n_len, i+2*n_len-1]
            # For each position j in 0..n_len-1:
            #   char1 = s[i+j] if i+j < n else '?' (can be anything)
            #   char2 = s[i+n_len+j] if i+n_len+j < n else '?' (can be anything)
            # If both are within original string s, they must be equal.
            # If one or both are outside, they can be chosen by Kolya to satisfy the condition.
            
            possible = True
            for j in range(n_len):
                idx1 = i + j
                idx2 = i + n_len + j
                
                c1 = s[idx1] if idx1 < n else None
                c2 = s[idx2] if idx2 < n else None
                
                if c1 is not None and c2 is not None:
                    if c1 != c2:
                        possible = False
                        break
                # If either is None, we can fill it with the needed character.
            
            if possible:
                if l > max_l:
                    max_l = l
                # Since we iterate n_len increasing, the first time we find a valid n_len for a specific start i,
                # it's not necessarily the global max, but we continue to check larger n_len later.
                # Actually, we want the maximum l, so we just update max_l whenever we find a valid one.
                # However, note that for a fixed i, if a tandem repeat of length 2*n is possible,
                # does it imply 2*(n-1) is also possible? Not necessarily at the same start, but we don't care.
                # We just need the max l found.

    print(max_l)

if __name__ == "__main__":
    solve()