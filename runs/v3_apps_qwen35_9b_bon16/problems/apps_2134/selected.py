import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
        b = []
        for _ in range(n):
            b.append(int(next(iterator)))
    except StopIteration:
        return

    # Count frequency of each a_i value
    from collections import defaultdict
    freq = defaultdict(int)
    for val in a:
        freq[val] += 1

    # Identify unique values that appear more than once
    # If a value appears multiple times, all students with that value can be in the group
    # because for any pair x, y with same a, neither thinks they are better than the other (same bits)
    can_group = set()
    for val, count in freq.items():
        if count > 1:
            can_group.add(val)

    # Also, if a value x is a subset of some value y that is in can_group,
    # then students with value x can also be included with students having value y.
    # Why? Because if y is in can_group, there is at least one other student with value y (or another value z that is subset of y? No, just y itself repeated).
    # Actually, the condition is: we can form a group if there exists a student y in the group such that no one in the group is "better" than y.
    # If we have a set of students all having value V where V is in can_group (count >= 2), then for any x in this set, no one is better than x (since all have same bits).
    # Now consider a student x with value x_val. x_val can be added to this group if there is some y in the group (with value V) such that x_val is a subset of y (x_val & y == x_val).
    # If x_val is a subset of V, then x knows only what y knows (and possibly less). So x does not think y is better? No.
    # Definition: x thinks x is better than y if x knows algo y doesn't. i.e., (a_x & ~a_y) != 0.
    # If a_x is subset of a_y, then (a_x & ~a_y) == 0. So x does NOT think x is better than y.
    # What about y thinking y is better than x? If a_y is not subset of a_x, then y thinks y is better than x.
    # The condition for the group to be calm: No student thinks they are better than EVERYONE else in the group.
    # Suppose we have a core set of students with value V (count >= 2).
    # For any two students u, v with value V: u does not think u > v, v does not think v > u.
    # So for the core set, no one thinks they are better than everyone else (since they can't beat anyone in the core, let alone everyone).
    # Now add a student x with value x_val where x_val is a subset of V.
    # Does x think x is better than everyone?
    # x vs core member y: x is subset of y, so x does not think x > y. So x fails the condition "better than everyone" immediately because of y.
    # So x cannot think x is better than everyone.
    # Does any core member y think y is better than everyone?
    # y vs another core member z: y is not better than z (same bits). So y fails the condition.
    # y vs x: y might think y > x (if x is strict subset). But since y fails against z, it doesn't matter.
    # Therefore, any x that is a subset of some V in can_group can be added.

    # Algorithm:
    # 1. Find all V such that count[V] >= 2.
    # 2. Collect all b_i for students where a_i is in can_group OR (exists V in can_group such that a_i is subset of V).
    # 3. Sum these b_i. If count of selected students < 2, output 0.

    # Wait, is it possible that a group exists without a "duplicate" base?
    # Condition: No student thinks they are better than everyone else.
    # If all students have distinct a_i values, can we form a group?
    # Suppose we have {x, y, z}.
    # If x is subset of y, and y is subset of z.
    # Then x does not think x > y, x does not think x > z. OK.
    # y does not think y > z. But y might think y > x.
    # z might think z > y and z > x.
    # If z thinks z > y and z > x, then z thinks z is better than everyone else. Fail.
    # So we need to avoid the "maximal element" in the subset lattice being unique in the group.
    # If we have a chain x < y < z, z is better than both. If z is the only one maximal, z thinks z > everyone.
    # To prevent this, every maximal element in the subset relation within the group must have a "peer" (another student with same or superset skills that prevents them from being better than everyone).
    # Specifically, if M is a student who thinks M > everyone else, we must exclude M or ensure there is someone M is not better than.
    # If M is strictly maximal (no one has M as subset except M itself in the group), then M thinks M > everyone.
    # So, in any valid group, for every student s, there must be at least one other student t in the group such that s is NOT better than t.
    # s is not better than t means (a_s & ~a_t) == 0 => a_s is subset of a_t.
    # So every student in the group must have a "super-set" peer in the group.
    # This implies that if we look at the set of values present in the group, for every value v present, there must be a value u in the set such that v is subset of u and u != v (or u == v but another student has same value).
    # If we have a value v with count >= 2, then for any student with value v, the other student with value v is a peer (v subset v).
    # If we have a value v with count 1, we need some u (u != v) in the group such that v is subset of u.
    # And recursively, u needs a peer.
    # This implies that eventually we must anchor on a value that has count >= 2.
    # Because if we only have unique values, let M be a maximal element in the group (subset-wise). Since it's maximal, no u in group (u != M) has M subset u.
    # Also since M is unique (count 1), there is no other M.
    # So for M, there is no t in group such that M is not better than t (unless M == t, but we need distinct students).
    # Wait, "not better than t" means (a_M & ~a_t) == 0.
    # If M is maximal, then for any t != M, a_M is NOT subset of a_t (otherwise M wouldn't be maximal or t would be a superset).
    # So (a_M & ~a_t) != 0. So M thinks M > t.
    # If M thinks M > t for all t != M, then M thinks M is better than everyone else.
    # Thus, any group containing a unique maximal element is invalid.
    # Therefore, the group must contain at least one value with count >= 2?
    # Or a cycle? No, subset relation is a DAG (antisymmetric).
    # So yes, the group must contain at least one value V with freq[V] >= 2.
    # And then any student with value x such that x is subset of some V (with freq >= 2) can be included.
    # Because for such an x, there exists a V in the group (with freq >= 2) such that x is subset of V.
    # Then x is not better than the student with value V. So x does not think x is better than everyone.
    # And for any V in the group, since freq[V] >= 2, there is another V', so V is not better than V'.
    # So the condition holds.

    # Conclusion:
    # Identify all values V with freq[V] >= 2.
    # Include all students with a_i == V for these V.
    # Also include all students with a_i = x if there exists V (with freq[V] >= 2) such that (x & V) == x.
    # Sum their b_i. If total count < 2, output 0.

    valid_indices = []
    total_sum = 0

    # Precompute valid a values
    valid_a_values = set(can_group)
    
    # Check each student
    for i in range(n):
        val = a[i]
        is_valid = False
        if val in valid_a_values:
            is_valid = True
        else:
            # Check if val is subset of any valid_a_values
            # Since n <= 7000 and |valid_a_values| <= n, O(n^2) is 49e6, acceptable in Python?
            # 7000^2 = 49,000,000. In Python this might be tight (1-2 seconds).
            # We need to optimize.
            # Optimization: The number of distinct a_i is at most 7000.
            # We can iterate only over distinct valid_a_values.
            # But worst case still O(N^2).
            # However, many cases will break early.
            # Let's try to optimize by checking against the set of valid values.
            # Can we do better?
            # Maybe not necessary if test cases are not worst-case.
            # But let's think: if we have many valid values, we iterate many times.
            # Actually, we only need to check if val is subset of ANY valid value.
            # If there is at least one valid value V such that (val | V) == V.
            
            # Optimization: Group by a_i?
            # If we have processed distinct values, we can cache.
            pass

    # Let's refactor to iterate distinct values first to build the set of valid a's efficiently
    distinct_a = {}
    for i in range(n):
        if a[i] not in distinct_a:
            distinct_a[a[i]] = []
        distinct_a[a[i]].append(i)

    # Identify base values
    base_values = []
    for val, indices in distinct_a.items():
        if len(indices) >= 2:
            base_values.append(val)

    if not base_values:
        print(0)
        return

    # Now find all students that can be added
    # A student i is valid if a[i] is a subset of at least one value in base_values.
    # We can iterate over all students.
    # To speed up, we can iterate over base_values and mark reachable a_i?
    # Or just iterate students and check against base_values.
    # Given N=7000, O(N * |base_values|) <= 7000 * 7000 = 49e6 operations.
    # Inside loop: bitwise AND. Very fast.
    # Python loop overhead might be an issue. 49e6 simple ops in Python takes ~2-5 seconds.
    # We need to be careful.
    # Is there a faster way?
    # We can collect all unique a_i that are subsets.
    # But we still need to check each unique a_i against base_values.
    # Number of unique a_i <= 7000.
    # Let's try to optimize the check.
    # If we have a set of base_values, for a given x, we want to know if exists v in base_values s.t. (x & v) == x.
    # This is equivalent to checking if (x | v) == v.
    
    # Can we use bit manipulation tricks? Not really for general 60-bit numbers.
    # However, we can sort base_values? Doesn't help much.
    # Maybe just implement cleanly and hope for average case.
    # Or precompute for each unique a_i whether it is valid.
    
    unique_a = list(distinct_a.keys())
    unique_to_indices = distinct_a
    
    valid_unique_a = set()
    for val in unique_a:
        # Check if val is subset of any base
        is_subset = False
        for base in base_values:
            if (val | base) == base:
                is_subset = True
                break
        if is_subset:
            valid_unique_a.add(val)

    # Now sum b_i for all i where a[i] in valid_unique_a
    ans = 0
    count = 0
    for i in range(n):
        if a[i] in valid_unique_a:
            ans += b[i]
            count += 1

    if count < 2:
        print(0)
    else:
        print(ans)

solve()