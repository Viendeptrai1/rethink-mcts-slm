import sys

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        n = int(input_data[0].strip())
    except ValueError:
        return

    fragments = []
    for i in range(1, n + 1):
        fragments.append(input_data[i].strip())

    # Build the graph: for each fragment, find the unique next fragment if it exists
    # Edge A -> B exists if suffix of A (len >= 5) == prefix of B
    # Since overlaps are unique, each node has at most one outgoing edge.
    
    next_node = {}
    
    for i in range(n):
        src = fragments[i]
        found_next = -1
        for j in range(n):
            if i == j:
                continue
            dst = fragments[j]
            # Check overlap
            max_overlap = min(len(src), len(dst))
            overlap_len = 0
            # We need overlap length >= 5
            # Check from length 5 up to min(len(src), len(dst))
            # Actually, the problem says "a suffix... equal to a prefix". 
            # It implies there is exactly one such length if it exists, or we just need to find if any exists >=5.
            # Given the uniqueness guarantee, we can just check lengths from 5 to min_len.
            # If multiple lengths work, the problem says "exactly one way", implying unique pair or unique overlap length?
            # "two fragments that satisfy these criteria do so in exactly one way" -> likely means for a given pair, 
            # the overlap length is fixed or the connection is unique.
            # Let's find the longest valid overlap >= 5.
            
            valid_overlap = -1
            for l in range(5, max_overlap + 1):
                if src.endswith(dst[:l]):
                    valid_overlap = l
            
            if valid_overlap != -1:
                # If we already found a next, and this is a different one, that would violate uniqueness.
                # But we assume input guarantees uniqueness.
                # However, we must ensure we pick the correct one. 
                # The problem says "exactly one way", so if multiple lengths work for the same pair, 
                # it might be ambiguous? But the problem guarantees no ambiguity in the graph structure for optimal path.
                # Let's assume for a pair (A, B), if they overlap >=5, they form an edge.
                # If A overlaps with multiple Bs, that's a branching point.
                # If A overlaps with B with multiple lengths, the "exactly one way" likely refers to the edge existence being unique.
                # Let's just record the first valid one we find? No, we need to be careful.
                # Re-reading: "two fragments that satisfy these criteria do so in exactly one way".
                # This probably means: For any pair (A, B), there is at most one overlap length >= 5.
                # So we can just check if any overlap >= 5 exists.
                
                # Wait, if A="abcde" and B="cdefg", overlap is "cde" (3) - no.
                # If A="abcde" and B="bcdef", overlap "bcde" (4) - no.
                # If A="abcde" and B="cdefgh", overlap "cde" (3) - no.
                # We need >= 5.
                
                # Let's implement finding the overlap length.
                # If we find one >= 5, we set found_next = j.
                # If we find another one >= 5 with a different j, that's a branch.
                # If we find another one with same j but different length? The guarantee says "exactly one way", 
                # so likely only one length works for a pair.
                
                if found_next == -1:
                    found_next = j
                else:
                    # If we found another one, it's a branch.
                    # But the problem says "unique maximal-length sequence" is guaranteed if not ambiguous.
                    # And "no fragment is contained within another".
                    # We will build the graph and then find the longest path.
                    pass
        
        if found_next != -1:
            next_node[i] = found_next

    # Now we have a functional graph (each node has out-degree 0 or 1).
    # We need to find the longest path in this DAG.
    # Since it's a DAG (no cycles guaranteed), we can use DP with memoization.
    
    # dp[i] = length of the longest path starting at node i
    # path[i] = the next node in the longest path starting at i (for reconstruction)
    
    memo_len = {}
    memo_next = {}
    
    def get_longest_path_len(u):
        if u in memo_len:
            return memo_len[u]
        
        if u not in next_node:
            memo_len[u] = 1
            memo_next[u] = -1
            return 1
        
        v = next_node[u]
        length = 1 + get_longest_path_len(v)
        memo_len[u] = length
        memo_next[u] = v
        return length

    # Calculate longest path length for all nodes
    for i in range(n):
        get_longest_path_len(i)
    
    # Find the starting node that gives the maximum path length
    max_len = 0
    start_node = -1
    
    for i in range(n):
        if memo_len[i] > max_len:
            max_len = memo_len[i]
            start_node = i
        elif memo_len[i] == max_len:
            # If there are multiple starting nodes with the same max length,
            # we need to check if they lead to the same sequence or different ones.
            # The problem says "If there are two or more maximal-length sequences... output AMBIGUOUS".
            # So if we find another start node with same max_len, it might be ambiguous.
            # However, we need to verify if the sequences are actually different.
            # Given the constraints and problem type, usually multiple starts with same length implies ambiguity.
            # But let's be rigorous: reconstruct both and compare.
            pass
    
    if start_node == -1:
        # Should not happen as n >= 1
        print("AMBIGUOUS")
        return

    # Reconstruct the path from start_node
    path = []
    curr = start_node
    while curr != -1:
        path.append(curr)
        curr = memo_next[curr]
    
    # Check for ambiguity: are there other start nodes with the same max_len?
    ambiguous = False
    for i in range(n):
        if i != start_node and memo_len[i] == max_len:
            # Reconstruct path from i
            path2 = []
            curr2 = i
            while curr2 != -1:
                path2.append(curr2)
                curr2 = memo_next[curr2]
            
            # Compare paths
            if len(path) == len(path2):
                # Check if the sequences of fragments are different
                # Note: The problem defines the reconstruction based on the sequence of fragments.
                # If the sequence of fragment indices is different, it's ambiguous.
                if path != path2:
                    ambiguous = True
                    break
            else:
                # Different lengths? But we checked max_len.
                # Wait, memo_len is the length of the path (number of nodes).
                # So if memo_len is same, the number of nodes is same.
                # So len(path) must equal len(path2).
                ambiguous = True
                break
    
    if ambiguous:
        print("AMBIGUOUS")
    else:
        # Construct the result string
        # F1 || omega(F2) || ... || omega(FM)
        # omega(Fi) is Fi with the prefix of length >= 5 removed, where that prefix equals suffix of F(i-1)
        
        result_parts = [fragments[path[0]]]
        
        for idx in range(1, len(path)):
            prev_frag = fragments[path[idx-1]]
            curr_frag = fragments[path[idx]]
            
            # Find the overlap length
            # We know there is an overlap >= 5.
            # Find the specific length.
            max_ov = min(len(prev_frag), len(curr_frag))
            overlap_len = 0
            for l in range(5, max_ov + 1):
                if prev_frag.endswith(curr_frag[:l]):
                    overlap_len = l
            
            # Remove the overlapping prefix from curr_frag
            # The overlap is the suffix of prev_frag and prefix of curr_frag.
            # We remove the first 'overlap_len' characters of curr_frag.
            start_idx = overlap_len
            result_parts.append(curr_frag[start_idx:])
        
        print("".join(result_parts))

if __name__ == "__main__":
    solve()