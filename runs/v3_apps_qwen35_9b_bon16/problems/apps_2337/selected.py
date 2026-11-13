import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
            
        b = []
        for _ in range(m):
            b.append(int(next(iterator)))
    except StopIteration:
        return

    # Sort b (problem statement says it's sorted, but good practice to ensure)
    b.sort()
    
    # We need to satisfy requirements a_1, a_2, ..., a_n.
    # We have m problems with complexities b_1, ..., b_m.
    # We can simplify a problem from complexity c to any d <= c.
    # We want to minimize the number of new problems we add.
    # This is equivalent to maximizing the number of existing problems we can use.
    # However, simply matching greedily might not work if we don't pick the right existing problems.
    # Actually, this is a maximum matching problem in a bipartite graph, but we can solve it greedily.
    # Since a is sorted ascending and b is sorted ascending:
    # To satisfy a[i], we need an available problem with complexity >= a[i].
    # To maximize usage, we should try to satisfy the smallest requirement a[i] with the smallest available b[j] >= a[i].
    # Wait, let's re-evaluate.
    # If we use a large b[j] for a small a[i], we might waste a large capability.
    # If we use a large b[j] for a large a[k], it might be necessary.
    # Actually, the standard greedy approach for "assign smallest sufficient resource" works here.
    # For each requirement a[i] (from smallest to largest), try to find the smallest available b[j] such that b[j] >= a[i].
    # If found, we use b[j] to satisfy a[i]. If not, we must add a new problem.
    
    # Let's verify with an example.
    # a = [2, 3, 4], b = [1]
    # i=0, a[0]=2. Smallest b[j] >= 2? None. Add 1 new.
    # i=1, a[1]=3. Smallest b[j] >= 3? None. Add 1 new.
    # i=2, a[2]=4. Smallest b[j] >= 4? None. Add 1 new.
    # Total 3. Correct.
    
    # Example 2:
    # a = [1, 2, 3], b = [1, 1, 1, 1, 1]
    # i=0, a[0]=1. Smallest b[j] >= 1 is b[0]=1. Use it. Remaining b: [1,1,1,1]
    # i=1, a[1]=2. Smallest b[j] >= 2? None (all are 1). Add 1 new.
    # i=2, a[2]=3. Smallest b[j] >= 3? None. Add 1 new.
    # Total 2. Correct.
    
    # Example 1:
    # a = [1, 2, 3], b = [1, 2, 2, 3, 3]
    # i=0, a[0]=1. Smallest b[j] >= 1 is b[0]=1. Use it.
    # i=1, a[1]=2. Smallest b[j] >= 2 is b[1]=2. Use it.
    # i=2, a[2]=3. Smallest b[j] >= 3 is b[2]=2? No. b[3]=3. Use it.
    # Total 0. Correct.

    # Algorithm:
    # Pointers for a (i) and b (j).
    # Iterate i from 0 to n-1.
    # Move j forward until b[j] >= a[i] or j reaches m.
    # If b[j] >= a[i], we match them (increment i, increment j, mark b[j] as used).
    # If we run out of b (j == m), we can't match the remaining a[i...n-1].
    # But wait, simply moving j forward and consuming works because:
    # If b[j] >= a[i], since a is increasing, b[j] is also >= a[i+1], etc.
    # Is it always optimal to use the smallest sufficient b[j]?
    # Yes. Suppose we have a requirement X and two available problems Y1 < Y2 where Y1 >= X and Y2 >= X.
    # Using Y1 leaves Y2 for potentially larger requirements. Using Y2 leaves Y1 which is "weaker".
    # Since requirements are increasing, having a weaker problem available for future (larger) requirements is less helpful.
    # So greedy works.

    ans = 0
    j = 0
    # We will simulate using a set or boolean array to mark used b's? 
    # Actually, since we iterate j forward and only move it, once b[j] is used, we move to j+1.
    # So we don't need a separate used array. Just the pointer j is enough.
    # Wait, if we skip some b's? No, the strategy is: for current a[i], find the first unused b[j] >= a[i].
    # Since we process a in increasing order, the "first unused" will be the smallest available value >= a[i].
    # Because if there was a smaller available value >= a[i], it would have been encountered earlier?
    # No. Consider a=[5], b=[4, 6]. 
    # i=0, a[0]=5. j=0, b[0]=4 < 5. Increment j.
    # j=1, b[1]=6 >= 5. Match. j becomes 2.
    # This logic holds.
    
    # However, what if b has duplicates and we skip some?
    # a = [2, 2], b = [2, 2]
    # i=0, a[0]=2. j=0, b[0]=2 >= 2. Match. j=1.
    # i=1, a[1]=2. j=1, b[1]=2 >= 2. Match. j=2.
    # Works.
    
    # What if a = [2, 3], b = [2, 2, 3]
    # i=0, a[0]=2. j=0, b[0]=2 >= 2. Match. j=1.
    # i=1, a[1]=3. j=1, b[1]=2 < 3. j=2. b[2]=3 >= 3. Match. j=3.
    # Works.
    
    # Implementation detail:
    # We iterate i from 0 to n-1.
    # Inside, while j < m and b[j] < a[i]: j += 1
    # If j < m: we used b[j], so j += 1 (consume it).
    # Else: we need a new problem, ans += 1.
    
    # Wait, is it possible that skipping b[j] because b[j] < a[i] is correct, 
    # but later we realize we should have saved it? No, because b[j] < a[i] means it cannot satisfy a[i].
    # Since a is increasing, it also cannot satisfy a[i+1], a[i+2], etc.
    # So b[j] is useless for any remaining requirement if it's < a[i].
    # Therefore, skipping it is correct.
    
    for i in range(n):
        while j < m and b[j] < a[i]:
            j += 1
        
        if j < m:
            # Match found
            j += 1 # consume b[j]
        else:
            # No match found for a[i] and all subsequent a's (since b is exhausted)
            ans += 1
            
    print(ans)

if __name__ == '__main__':
    solve()