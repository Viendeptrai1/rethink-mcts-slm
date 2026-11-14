import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    k = int(input_data[0])
    q = input_data[1]

    if len(q) < k:
        print("NO")
        return

    used_chars = set()
    parts = []
    current_start = 0

    for i in range(len(q)):
        char = q[i]
        if char not in used_chars:
            if len(parts) == k:
                # We already have k parts, but we found a new starting character.
                # This means we cannot form exactly k parts with distinct starts
                # because we would need to split further, but splitting a part
                # doesn't change its starting character.
                # Actually, if we have k parts and find a new start, we can just
                # make the last part end before this new char and start a new one.
                # But we must ensure we don't exceed k parts.
                # Let's re-evaluate: we need exactly k parts.
                # Strategy: Collect k distinct starting characters.
                # Once we have k distinct starts, the remaining string goes to the last part.
                # However, the greedy approach of starting a new part immediately when
                # a new character is seen might create more than k parts if we are not careful.
                # Correct logic:
                # We need to select k indices i_1, i_2, ..., i_k such that q[i_j] are distinct
                # and i_1 < i_2 < ... < i_k, and i_1 = 0.
                # Then the parts are q[i_1:i_2], q[i_2:i_3], ..., q[i_k:].
                # So we just need to find k distinct characters starting from index 0.
                # The first part must start at 0.
                # We scan and pick the next distinct character as the start of the next part.
                # If we find k distinct characters, we are good.
                # If we finish the string and haven't found k distinct characters, then NO.
                pass
            
            # If we haven't collected k parts yet, start a new part
            if len(parts) < k:
                # Add the current part from current_start to i
                if len(parts) > 0:
                    # This logic is flawed in the loop above. Let's restart the logic cleanly.
                    pass
        
        # Let's rewrite the logic inside the loop properly.
        pass

    # Refined Logic:
    # We need exactly k substrings.
    # Substring 1 starts at index 0.
    # Substring 2 starts at some index i2 > 0, with q[i2] != q[0].
    # Substring 3 starts at some index i3 > i2, with q[i3] != q[0] and q[i3] != q[i2].
    # ...
    # Substring k starts at some index ik > i(k-1), with q[ik] distinct from previous starts.
    # The last substring goes until the end of the string.
    # So we just need to find k indices: 0 = p1 < p2 < ... < pk <= len(q)
    # such that q[p1], q[p2], ..., q[pk] are all distinct.
    # Note: pk can be equal to len(q) if we consider the start of a hypothetical (k+1)-th part,
    # but actually the k-th part starts at pk and goes to end. So pk must be < len(q) unless k=1?
    # Wait, if k=1, p1=0, part is q[0:]. Correct.
    # If k>1, pk must be < len(q) because the k-th part must have at least length 1?
    # The problem says "sequence of k strings". It doesn't explicitly say non-empty, but usually strings in such problems are non-empty.
    # "concatenation ... is string q". If a string is empty, it doesn't contribute characters.
    # However, the condition "first characters ... are distinct" implies the strings must have a first character, so they must be non-empty.
    # Therefore, each part must have length >= 1.
    # This implies p1=0, p2 > p1, ..., pk > p(k-1), and pk < len(q) (since the k-th part is q[pk:] and must be non-empty).
    # So we need to find k distinct characters at indices 0 = p1 < p2 < ... < pk < len(q).
    
    used = set()
    starts = []
    current_idx = 0
    
    # We need to find k starting positions.
    # The first one is always 0.
    if q[0] in used:
        # Should not happen initially
        pass
    used.add(q[0])
    starts.append(0)
    
    count = 1
    while count < k:
        current_idx += 1
        if current_idx >= len(q):
            break
        char = q[current_idx]
        if char not in used:
            used.add(char)
            starts.append(current_idx)
            count += 1
    
    if count < k:
        print("NO")
    else:
        print("YES")
        for i in range(k):
            start = starts[i]
            if i == k - 1:
                end = len(q)
            else:
                end = starts[i+1]
            print(q[start:end])

if __name__ == "__main__":
    solve()