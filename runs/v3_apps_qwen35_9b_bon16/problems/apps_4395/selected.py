import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # There are 3 colors: R, G, B. We can represent them as 0, 1, 2.
    # A nice garland must have the property that if t[i] == t[j], then |i-j| % 3 == 0.
    # This implies that the color at index i depends only on i % 3.
    # Specifically, indices with the same remainder modulo 3 must all have the same color.
    # So the garland is determined by assigning one color to remainder 0, one to remainder 1, and one to remainder 2.
    # These three assigned colors must be distinct (otherwise, two different remainder classes would share a color,
    # and since the remainders are different, the distance between some lamps of that color would not be divisible by 3).
    # Actually, let's re-verify: if we assign color C to remainder r1 and color C to remainder r2 (where r1 != r2),
    # then a lamp at index i (i % 3 == r1) and a lamp at index j (j % 3 == r2) both have color C.
    # The distance |i - j| mod 3 = |(r1 - r2)| mod 3 = 0 only if r1 = r2.
    # Since r1 != r2, |i-j| is not divisible by 3. Thus, the colors assigned to the three remainder classes MUST be distinct.
    
    # Therefore, the nice garland must be a permutation of "RGB" repeated.
    # The possible patterns are the 3! = 6 permutations of "RGB" assigned to positions 0, 1, 2 mod 3.
    # The permutations are:
    # 1. RGBRGB... (0->R, 1->G, 2->B)
    # 2. RBGRBG... (0->R, 1->B, 2->G)
    # 3. GRBG...   (0->G, 1->R, 2->B)
    # 4. GBGR...   (0->G, 1->B, 2->R)
    # 5. BRGB...   (0->B, 1->R, 2->G)
    # 6. BG RB...   (0->B, 1->G, 2->R)
    
    # We can generate these 6 base strings and count the mismatches with the input string s.
    # The one with the minimum mismatches is our answer.
    
    colors = ['R', 'G', 'B']
    perms = []
    
    from itertools import permutations
    for p in permutations(colors):
        base = p[0] + p[1] + p[2]
        perms.append(base)
    
    min_changes = n + 1
    best_pattern = ""
    
    for p in perms:
        # Construct the candidate string
        cand = []
        for i in range(n):
            cand.append(p[i % 3])
        cand_str = "".join(cand)
        
        # Calculate changes
        changes = 0
        for i in range(n):
            if s[i] != cand_str[i]:
                changes += 1
        
        if changes < min_changes:
            min_changes = changes
            best_pattern = cand_str
    
    print(min_changes)
    print(best_pattern)

if __name__ == "__main__":
    solve()