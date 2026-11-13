import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        
        k = int(input_data[0])
        q = input_data[1]
    except IndexError:
        return

    if len(q) < k:
        print("NO")
        return

    distinct_chars = set()
    result = []
    current_start = 0
    used_count = 0

    for i in range(len(q)):
        char = q[i]
        if char in distinct_chars:
            if used_count == k - 1:
                # We have already formed k-1 strings with distinct starting characters.
                # The remaining characters (from current_start to i-1) form the last string.
                # However, we must ensure that the starting character of the last string (q[current_start])
                # is not in distinct_chars. But since we are iterating and only checking 'char' at 'i',
                # and we stopped because 'char' (at i) is a duplicate, it means q[current_start] was already processed.
                # Actually, the logic is: if we encounter a duplicate start character before we have k strings,
                # we can't include it as a new string start. But we can just append everything from current_start to i-1
                # as the last string, provided we haven't exceeded k.
                
                # Wait, the condition is: we need exactly k strings.
                # If we have used_count == k-1, it means we have formed k-1 strings.
                # The current position 'i' has a character that is already a start of a previous string.
                # So we cannot start a new string at 'i'. Therefore, the last string must end at i-1?
                # No, the last string can extend to the end of q.
                # The issue is that we need to partition q into k strings such that their first chars are distinct.
                # If we greedily take the shortest possible prefixes for the first k-1 strings,
                # and then the rest is the k-th string, we just need to check if the k-th string's first char is distinct.
                
                # Let's refine the greedy approach:
                # We need to find k split points.
                # Let the split points be indices 0 = p0 < p1 < ... < pk = len(q).
                # The strings are q[p0:p1], q[p1:p2], ..., q[pk-1:pk].
                # The condition is: q[p0], q[p1], ..., q[pk-1] are all distinct.
                
                # We can greedily pick the first occurrence of each character from the set of available characters.
                # We need to pick k distinct characters to be the starts of our k strings.
                # Once we pick a character at index i as a start, the next string will start at some j > i.
                # To maximize our chances, we should make the current string as short as possible?
                # Actually, the position of the next start doesn't matter for the distinctness of the current start,
                # but it matters for which characters are available later.
                # However, since we just need ANY valid sequence, we can try to pick the earliest possible occurrences
                # of k distinct characters.
                
                # Algorithm:
                # 1. Identify the indices of the first occurrence of each character present in q.
                # 2. If the number of unique characters in q is less than k, output NO.
                # 3. Pick any k distinct characters. To make it easy, let's pick the first k distinct characters we encounter in q.
                #    Let their indices be idx1, idx2, ..., idxk. Note that idx1 < idx2 < ... < idxk because we scan left to right.
                # 4. We will form k strings. The first string starts at idx1. The second at idx2, etc. The k-th at idxk.
                #    But wait, the strings must cover the whole string q.
                #    So:
                #    String 1: from start (0) to idx2-1? No.
                #    The first string MUST start at 0. So the first character of the first string is q[0].
                #    This fixes the first start character to be q[0].
                #    Then we need to find k-1 more distinct characters that appear AFTER q[0] (or at least after the end of the first string).
                #    Actually, the split points are fixed by the starts of the subsequent strings.
                #    If the i-th string starts at index s_i, then the (i-1)-th string ends at s_i - 1.
                #    The first string starts at 0. So s_1 = 0.
                #    We need to choose s_2, s_3, ..., s_k such that 0 < s_2 < s_3 < ... < s_k < len(q) (actually s_k <= len(q), but the string is q[s_k:]).
                #    Wait, if s_k is the start of the k-th string, the k-th string is q[s_k:].
                #    The condition is that q[0], q[s_2], q[s_3], ..., q[s_k] are distinct.
                #    We need to find k-1 indices s_2, ..., s_k such that q[s_i] are distinct and distinct from q[0].
                #    To maximize the chance of finding such indices, we should pick the earliest possible occurrences of distinct characters.
                #    
                #    Revised Algorithm:
                #    1. We MUST have the first string start at 0. So char1 = q[0].
                #    2. We need to find k-1 other indices i_2, i_3, ..., i_k such that:
                #       0 < i_2 < i_3 < ... < i_k < len(q)
                #       q[i_2], q[i_3], ..., q[i_k] are distinct and none equal q[0].
                #    3. If we can't find k-1 such characters, output NO.
                #    4. If we find them, we can set the split points as:
                #       s_1 = 0
                #       s_2 = i_2
                #       s_3 = i_3
                #       ...
                #       s_k = i_k
                #       And the k-th string goes to the end of q.
                #       The strings are:
                #       s_1: q[0:i_2]
                #       s_2: q[i_2:i_3]
                #       ...
                #       s_{k-1}: q[i_{k-1}:i_k]
                #       s_k: q[i_k:]
                #       This works because the start of s_1 is q[0], start of s_2 is q[i_2], ..., start of s_k is q[i_k].
                #       All these starts are distinct by our selection.
                #       And they cover the whole string because the intervals are contiguous and the last one goes to end.
                
                pass

    # Re-implementing cleanly based on the logic above:
    n = len(q)
    if n < k:
        print("NO")
        return

    # The first string must start at 0.
    first_char = q[0]
    
    # We need to find k-1 other indices after 0 (strictly increasing) with distinct characters different from first_char.
    # Let's collect the indices of the first occurrence of every character in q.
    first_occurrence = {}
    for idx, char in enumerate(q):
        if char not in first_occurrence:
            first_occurrence[char] = idx

    # We need k distinct characters. One of them MUST be q[0].
    # If q[0] is not in the set of characters available later? No, q[0] is the start of the first string.
    # We need to pick k-1 other characters from the unique characters in q, excluding q[0], such that their first occurrence index is > 0.
    # Actually, any character appearing in q after index 0 can be a start of a subsequent string.
    # But we need their indices to be strictly increasing.
    # The easiest way is to iterate through the string starting from index 1 and pick the first k-1 distinct characters we see that are not q[0].
    
    available_chars = set()
    selected_indices = [0] # Index of the start of the first string
    selected_starts = [first_char]
    
    current_idx = 1
    count_needed = k - 1
    
    while current_idx < n and count_needed > 0:
        char = q[current_idx]
        if char not in selected_starts:
            # We can use this character as the start of a new string
            selected_indices.append(current_idx)
            selected_starts.append(char)
            count_needed -= 1
        current_idx += 1
    
    if count_needed > 0:
        print("NO")
        return
    
    # Now we have k split points: selected_indices[0]...selected_indices[k-1]
    # selected_indices[0] is 0.
    # The strings are:
    # s_0: from selected_indices[0] to selected_indices[1]
    # s_1: from selected_indices[1] to selected_indices[2]
    # ...
    # s_{k-1}: from selected_indices[k-1] to end
    
    parts = []
    for i in range(k):
        start = selected_indices[i]
        if i == k - 1:
            end = n
        else:
            end = selected_indices[i+1]
        parts.append(q[start:end])
    
    print("YES")
    for part in parts:
        print(part)

if __name__ == "__main__":
    solve()