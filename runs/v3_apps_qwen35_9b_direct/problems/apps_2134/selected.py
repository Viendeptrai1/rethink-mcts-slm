import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
    
    b = []
    for _ in range(n):
        b.append(int(next(iterator)))
    
    # Identify students who are part of a "maximal" set
    # A student i is in the maximal set if there exists another student j such that (a[i] | a[j]) == a[i]
    # This means a[j] is a subset of a[i] (all bits set in a[j] are also set in a[i]).
    # If a student is in the maximal set, they can be part of a valid group.
    # Specifically, if we take all students who are in the maximal set, no one in this group thinks they are better than everyone else.
    # Why? Let S be the set of students in the maximal set.
    # For any x in S, there exists y in S such that a[y] is a subset of a[x].
    # If x thinks they are better than everyone in S, then for all z in S, x knows an algorithm z doesn't.
    # But if there is a y in S such that a[y] is a subset of a[x], then y knows only what x knows (and possibly less).
    # So x does NOT know an algorithm that y doesn't know? Wait, the condition is: x thinks better than y if x knows algo y doesn't.
    # If a[y] is a subset of a[x], then every algo y knows, x knows. So x does NOT think better than y.
    # Therefore, x cannot think they are better than EVERYONE in S, because they don't think better than y.
    # Thus, the set of all "maximal" students forms a valid group.
    
    # We need to find all i such that there exists j != i with (a[i] | a[j]) == a[i].
    # Note: if a[i] == a[j], then (a[i] | a[j]) == a[i] holds.
    
    # Algorithm:
    # 1. Count frequencies of each distinct a value.
    # 2. For each distinct value v, if count[v] > 1, then all students with a[i] == v are in the maximal set.
    # 3. For each distinct value v with count[v] == 1, check if there exists another value u (u != v) such that (v | u) == v.
    #    If so, the student with a[i] == v is in the maximal set.
    
    # Since n <= 7000, we can do an O(n^2) check or optimize.
    # Given n=7000, O(n^2) is 49 million, which might be tight in Python but acceptable if operations are simple.
    # However, we can optimize by grouping identical a's first.
    
    from collections import defaultdict
    
    val_counts = defaultdict(int)
    for x in a:
        val_counts[x] += 1
        
    # Identify indices that belong to the maximal set
    in_maximal = [False] * n
    
    # Step 1: Handle duplicates
    # If a value appears more than once, all its instances are in the maximal set.
    for i in range(n):
        if val_counts[a[i]] > 1:
            in_maximal[i] = True
            
    # Step 2: Handle unique values
    # For each unique value v, check if it is a superset of any other value u present in the array.
    # We only need to check against other values present in the array.
    
    # Let's collect unique values and their indices
    unique_vals = list(val_counts.keys())
    
    # Optimization: If we have many unique values, O(n^2) on unique values might be slower than on n if n is small, 
    # but here n is up to 7000. The number of unique values is at most 7000.
    # Let's just iterate.
    
    # To speed up, we can precompute which values are "covered" by others.
    # Actually, simply iterating over all pairs of unique values is O(U^2) where U is number of unique values.
    # U <= 7000. 7000^2 = 49,000,000. In Python, this might take a few seconds.
    # We need to be careful. Let's try to optimize.
    
    # Alternative approach:
    # For each unique value v, we want to know if there exists u in unique_vals such that (v | u) == v and u != v.
    # This is equivalent to: is there any u in unique_vals such that (v & u) == u and u != v?
    # Or simply: is there any u in unique_vals such that u is a proper subset of v?
    
    # Let's try the O(U^2) approach first but break early if possible? No, we need to check all.
    # Maybe we can reduce the set of candidates?
    # If we sort unique values, does it help? Not really for subset check.
    
    # Let's reconsider the constraints. N=7000. Time limit is usually 1-2 seconds.
    # Python might struggle with 50M iterations.
    # Is there a faster way?
    # We can use the fact that if v is a superset of u, and u is a superset of w, then v is a superset of w.
    # But we just need existence.
    
    # Let's try to optimize the check.
    # We can iterate over all unique values u, and for each u, mark all v such that (v | u) == v.
    # Then any v that gets marked is in the maximal set.
    # This is still O(U^2).
    
    # Wait, if we have many duplicates, U is small. If all are unique, U is large.
    # If all are unique, we must check pairs.
    # Is there a property we can exploit?
    # Maybe we can skip checking if we already found a superset?
    # For a specific v, as soon as we find one u such that u is subset of v, we mark v and move on.
    # This might help on average.
    
    # Let's implement the O(U^2) with early break.
    
    # Map value to list of indices
    val_to_indices = defaultdict(list)
    for i in range(n):
        val_to_indices[a[i]].append(i)
        
    # We will mark indices
    # Initialize a set of indices to include
    included_indices = set()
    
    # Add all with duplicates
    for val, count in val_counts.items():
        if count > 1:
            for idx in val_to_indices[val]:
                included_indices.add(idx)
                
    # Now check unique values
    # We only need to check values that are currently not in included_indices
    # But we need to check against ALL values in the array to see if they are subsets.
    
    # Let's create a list of unique values to iterate
    unique_list = list(val_counts.keys())
    
    # To optimize, we can iterate over each unique value u, and for each other unique value v,
    # check if u is a subset of v.
    # If u is a subset of v, then v is in the maximal set.
    
    # We can do:
    # for u in unique_list:
    #    for v in unique_list:
    #        if u != v and (v | u) == v:
    #            mark v
    
    # This is O(U^2). Let's hope the constant factor is small or test cases are weak.
    # Or maybe we can optimize by noting that if u is a subset of v, then u is also a subset of any superset of v.
    # But we don't know supersets beforehand.
    
    # Let's try to code it efficiently.
    
    # Precompute a boolean array for unique values?
    # Let's assign an ID to each unique value.
    # unique_vals = sorted(unique_list) # Sorting might help with cache? Not really.
    
    # Let's just do the double loop with early break for v.
    # For each v, we want to find if there exists u != v such that (v | u) == v.
    # We can iterate u over unique_list.
    
    # Optimization: If we find one such u, we stop for v.
    
    # Also, we can skip v if it's already marked.
    
    # Let's refine:
    # We have a set `marked` of values (or indices) that are in the maximal set.
    # Initially, marked contains all values with count > 1.
    # Then for each value v not in marked:
    #    check if there exists u in unique_list such that u != v and (v | u) == v.
    #    If yes, add v to marked.
    
    # This is still O(U^2) in worst case (e.g., chain of subsets or no subsets).
    # But with early break, it might be faster.
    
    marked_values = set()
    for val, count in val_counts.items():
        if count > 1:
            marked_values.add(val)
            
    # Now iterate over unique values that are not yet marked
    for v in unique_list:
        if v in marked_values:
            continue
        
        # Check if v is a superset of any other u
        found = False
        for u in unique_list:
            if u == v:
                continue
            if (v | u) == v:
                found = True
                break
        if found:
            marked_values.add(v)
            
    # Now sum b[i] for all i where a[i] is in marked_values
    total_skill = 0
    for i in range(n):
        if a[i] in marked_values:
            total_skill += b[i]
            
    # The problem requires a group of at least two students.
    # If the number of students in the maximal set is less than 2, output 0.
    count_in_group = 0
    for i in range(n):
        if a[i] in marked_values:
            count_in_group += 1
            
    if count_in_group < 2:
        print(0)
    else:
        print(total_skill)

if __name__ == '__main__':
    solve()