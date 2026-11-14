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
    
    # Count frequency of each a_i
    from collections import Counter
    counts = Counter(a)
    
    # Identify students whose skill set is a subset of some other student's skill set
    # Specifically, if a[i] == a[j] and i != j, then both are subsets of each other.
    # If a[i] is a proper subset of a[j], then i is a subset of j.
    # We want to find all i such that there exists j != i where (a[i] & a[j]) == a[i].
    # This condition (a[i] | a[j]) == a[j] means a[i] is a subset of a[j].
    
    valid_indices = set()
    
    # Optimization: Group by identical a values first
    # If a group has size >= 2, all members in that group are valid relative to each other.
    for val, count in counts.items():
        if count >= 2:
            # All students with this exact value are valid
            for i in range(n):
                if a[i] == val:
                    valid_indices.add(i)
    
    # Now check for proper subsets against the "core" group
    # The core group consists of all students who have a value that appears >= 2 times.
    # Any student whose a[i] is a subset of any value in the core group is also valid.
    
    core_values = set()
    for val, count in counts.items():
        if count >= 2:
            core_values.add(val)
    
    # If there are no core values, no group of size >= 2 can be formed where everyone is a subset of someone else?
    # Actually, if no value appears twice, can we have a valid group?
    # If all a_i are distinct, then for any pair (i, j), if a[i] is subset of a[j], then a[i] != a[j].
    # But if a[i] is a subset of a[j] and a[j] is a subset of a[i], then a[i] == a[j].
    # So if all are distinct, we can't have mutual subsets.
    # However, the condition is: no student thinks they are better than everyone else.
    # Student i thinks they are better than j if (a[i] & ~a[j]) != 0.
    # i thinks they are better than EVERYONE in group G if for all j in G, j != i, (a[i] & ~a[j]) != 0.
    # This is equivalent to: a[i] is NOT a subset of a[j] for any j in G.
    # So the condition "no student thinks they are better than everyone else" means:
    # For every i in G, there exists at least one j in G (j != i) such that a[i] is a subset of a[j].
    
    # If we have a set of students where for every i, there is a j (j!=i) with a[i] subset a[j], then it's valid.
    # Strategy:
    # 1. Find all "maximal" elements in the group. If a group has a unique maximal element (in terms of set inclusion),
    #    then that element is NOT a subset of anyone else in the group, so that element thinks they are better than everyone else.
    #    Thus, a valid group cannot have a unique maximal element.
    # 2. Actually, if we take all students whose a[i] is a subset of some "popular" value (count >= 2), then for any such student i,
    #    there exists a j with a[j] == popular_value (and j != i because count >= 2) such that a[i] subset a[j].
    #    So the condition is satisfied for all i in this set.
    # 3. Can we add more students? Suppose we have a set S of students where for every i in S, there exists j in S, j!=i, a[i] subset a[j].
    #    This is exactly the condition.
    #    Notice that if we have a "core" set C where every element in C appears at least twice, then for any x in C, there is y in C, y!=x with x==y (subset).
    #    If we add a student z such that a[z] is a subset of some c in C, then for z, we have c (or another copy of c) as a superset.
    #    And for c in C, we still have the other copy of c.
    #    So the union of all students whose a[i] is a subset of any value that appears >= 2 times forms a valid group.
    
    # Let's verify:
    # Let S = { i | exists v in core_values such that (a[i] | v) == v }
    # For any i in S:
    #   There exists v in core_values such that a[i] subset v.
    #   Since v is in core_values, there are at least two indices p, q such that a[p] == v and a[q] == v.
    #   If i == p, then q is in S (since v is subset of v) and q != i, and a[i] subset a[q].
    #   If i != p, then p is in S and p != i, and a[i] subset a[p].
    #   So for every i in S, there is a j in S, j != i, such that a[i] subset a[j].
    #   Therefore, no student in S thinks they are better than everyone else in S.
    #   Also, |S| >= 2 because core_values is not empty (if it is, we can't form a group of size >= 2? Wait).
    #   If core_values is empty, then no value appears >= 2 times.
    #   In that case, can we have a valid group?
    #   If all a_i are distinct, then for any i, if a[i] is a subset of a[j], then a[i] != a[j].
    #   If we have a chain i1 -> i2 -> ... -> ik where a[i1] subset a[i2] subset ... subset a[ik].
    #   Then for i1, i2 is a superset. For i2, i3 is a superset. ... For ik, is there a superset?
    #   If ik is the unique maximal element, then ik thinks they are better than everyone else (since they are not a subset of anyone else in the group).
    #   So the group is invalid.
    #   To be valid, every element must have a strict superset in the group (or an equal one).
    #   If all are distinct, we can't have cycles of equality. So we must have a chain ending in a maximal element.
    #   That maximal element has no superset in the group, so it thinks it's better than everyone else.
    #   Therefore, if all a_i are distinct, no valid group of size >= 2 exists.
    #   So we only care about the case where at least one value appears >= 2 times.
    
    if not core_values:
        print(0)
        return
    
    total_skill = 0
    for i in range(n):
        is_subset = False
        for v in core_values:
            if (a[i] | v) == v:
                is_subset = True
                break
        if is_subset:
            total_skill += b[i]
    
    print(total_skill)

if __name__ == '__main__':
    solve()