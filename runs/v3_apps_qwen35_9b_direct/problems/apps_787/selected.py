import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    k = int(input_data[0])
    q = input_data[1]

    if k > len(q):
        print("NO")
        return

    seen = set()
    parts = []
    start = 0

    for i in range(k):
        if start >= len(q):
            print("NO")
            return

        char = q[start]
        if char in seen:
            print("NO")
            return
        seen.add(char)

        # Find the end of the current part
        end = start
        while end < len(q) and end < start + (len(q) - start) // (k - i):
            end += 1

        # Greedy approach: take as much as possible but ensure we can finish
        # Actually, a simpler greedy: take the minimal needed to get a new char? 
        # No, the problem just requires distinct first chars. We can take any split as long as first chars are distinct.
        # Strategy: For each of the k parts, take the substring starting at 'start' until we either:
        # 1. Reach the end of the string (only possible if this is the last part)
        # 2. Or we decide to stop. But we need to ensure we can form k parts.
        #
        # Better strategy:
        # We need to pick k starting positions p_0, p_1, ..., p_{k-1} such that:
        # p_0 = 0
        # p_{i+1} > p_i
        # p_k = len(q)
        # and q[p_i] are all distinct.
        #
        # We can greedily pick the next starting position as the first occurrence of a new character
        # that hasn't been used yet, but we must ensure that after picking k such positions, we can cover the whole string.
        # Actually, the simplest valid construction:
        # Let's collect the indices of all unique characters in order of appearance.
        # If the number of unique characters is less than k, then impossible -> NO.
        # If >= k, we can pick the first k unique characters' first occurrences as our split points.
        # Then the parts are:
        # s_1 = q[0 : p_1]
        # s_2 = q[p_1 : p_2]
        # ...
        # s_k = q[p_{k-1} : len(q)]
        #
        # Wait, the split points must be the START of each string.
        # So if we choose indices idx_0, idx_1, ..., idx_{k-1} as the start of each string:
        # idx_0 must be 0.
        # idx_1 > idx_0, idx_2 > idx_1, ..., idx_{k-1} > idx_{k-2}.
        # And idx_{k-1} must be < len(q) (so that s_k is non-empty).
        # The last string s_k will be q[idx_{k-1} : len(q)].
        #
        # Algorithm:
        # 1. Identify the first occurrence of each character in q.
        # 2. Collect these first occurrences in a list, sorted by index.
        # 3. If the number of unique characters is less than k, output NO.
        # 4. Otherwise, take the first k indices from this sorted list. Let them be p_0, p_1, ..., p_{k-1}.
        #    Note: p_0 will be 0.
        # 5. Construct the strings:
        #    s_1 = q[p_0 : p_1]
        #    s_2 = q[p_1 : p_2]
        #    ...
        #    s_k = q[p_{k-1} : len(q)]
        # 6. Verify that the first characters are distinct (they are, by construction) and that the concatenation is q (by definition of splits).
        #    Also verify that each part is non-empty. Since p_{i+1} > p_i, s_1...s_{k-1} are non-empty.
        #    s_k is non-empty because p_{k-1} < len(q) (since we picked first occurrences and there are at least k unique chars, 
        #    the k-th unique char must appear before the end, or at least we have k distinct chars so the last one is at some index < len(q)).
        #    Actually, if the k-th unique char is at index X, then X < len(q) is guaranteed because it's an index in the string.
        
        unique_first_indices = []
        seen_chars = set()
        for idx, char in enumerate(q):
            if char not in seen_chars:
                seen_chars.add(char)
                unique_first_indices.append(idx)
                if len(unique_first_indices) == k:
                    break
        
        if len(unique_first_indices) < k:
            print("NO")
            return
        
        # We have at least k unique characters. Take the first k first-occurrence indices.
        split_points = unique_first_indices[:k]
        
        # Construct the result
        result_parts = []
        current = 0
        for i in range(k):
            start_idx = split_points[i]
            # The part starts at start_idx
            # The next part starts at split_points[i+1] if exists, else end of string
            if i < k - 1:
                end_idx = split_points[i+1]
            else:
                end_idx = len(q)
            
            # The part is q[start_idx : end_idx]
            # But wait, the previous part ended at split_points[i]. 
            # So the current part should start at split_points[i] and go up to split_points[i+1] (exclusive).
            # However, we need to make sure we don't overlap or skip.
            # The split points are the START indices of the k strings.
            # String 1 starts at split_points[0] (which is 0) and ends at split_points[1].
            # String 2 starts at split_points[1] and ends at split_points[2].
            # ...
            # String k starts at split_points[k-1] and ends at len(q).
            
            # Check if the previous part ended exactly where this one starts.
            # Yes, by definition.
            
            # But we must ensure that the part is non-empty.
            # Since split_points is strictly increasing (indices in string), split_points[i+1] > split_points[i].
            # So the slice [split_points[i] : split_points[i+1]] is non-empty.
            # For the last part, [split_points[k-1] : len(q)] is non-empty because split_points[k-1] < len(q).
            
            part = q[start_idx : end_idx]
            result_parts.append(part)
        
        print("YES")
        for part in result_parts:
            print(part)

if __name__ == "__main__":
    solve()