import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    a = []
    for i in range(n):
        a.append(int(data[2 + i]))
    
    b = []
    for i in range(m):
        b.append(int(data[2 + n + i]))
    
    # Sort b just in case, though problem statement says it's sorted
    b.sort()
    
    # We need to cover all requirements in a.
    # Strategy: Greedily match the smallest available requirement with the smallest available problem that can cover it.
    # Since we can only simplify (reduce complexity), a problem with complexity B can cover a requirement A if B >= A.
    # To minimize extra problems, we should use existing problems to cover as many requirements as possible.
    # The optimal greedy strategy:
    # Iterate through requirements a_1, a_2, ... a_n.
    # For each requirement, try to find the smallest available problem in b that is >= requirement.
    # If found, use it (remove from b) and move to next requirement.
    # If not found, we must create a new problem (increment answer) and move to next requirement.
    
    # Since both arrays are sorted, we can use two pointers or a simple iteration.
    # Let's sort a as well to ensure we process smallest requirements first (though input says a is sorted).
    a.sort()
    
    # We will simulate the process
    # Pointer for b
    b_idx = 0
    b_count = m
    extra_needed = 0
    
    # We need to cover n requirements
    for req in a:
        # Find the smallest problem in b that is >= req
        # Since b is sorted, we can advance b_idx until b[b_idx] >= req
        # But we need to be careful not to reuse problems.
        # Actually, since we want the smallest valid problem to save larger ones for larger requirements,
        # we should pick the first available problem in b that is >= req.
        
        # However, simply iterating might be O(N*M) if not careful, but N, M <= 3000, so O(N*M) is 9*10^6, acceptable.
        # But we can do better with two pointers.
        
        # Let's refine the two pointer approach:
        # We iterate through requirements. For each requirement, we look at the current smallest available problem.
        # If current problem < requirement, it cannot cover this requirement (nor any larger one), so it's useless for requirements.
        # Wait, if current problem < requirement, it can't cover this requirement. Can it cover a smaller one?
        # We are processing requirements in increasing order. So if current problem < current requirement, 
        # it was also < previous requirements (which we already processed). So this problem is useless.
        # So we skip it.
        
        # If current problem >= requirement, we can use it. Should we?
        # Yes, because using the smallest valid problem is optimal (saves larger problems for larger requirements).
        
        # So algorithm:
        # 1. Filter out problems in b that are smaller than the current requirement? 
        #    No, because a requirement increases. A problem that was too small for req_i might be too small for req_{i+1}.
        #    Actually, if b[j] < a[i], then b[j] < a[i+1] as well. So such problems are useless for all future requirements.
        #    So we can discard them.
        
        # Revised Two Pointer:
        # i = index for a
        # j = index for b
        # while i < n:
        #   if j < m and b[j] < a[i]:
        #       j += 1  # This problem is too small for current requirement and all future ones, discard
        #   elif j < m and b[j] >= a[i]:
        #       # Match found
        #       j += 1  # Use this problem
        #       i += 1  # Move to next requirement
        #   else:
        #       # No more problems in b that can cover a[i]
        #       extra_needed += 1
        #       i += 1  # Must create a new problem
        
        # Let's trace:
        # a = [1, 2, 3], b = [1, 1, 1, 1, 1]
        # i=0, req=1. j=0, b[0]=1 >= 1. Match. j=1, i=1.
        # i=1, req=2. j=1, b[1]=1 < 2. Skip b[1]. j=2.
        # j=2, b[2]=1 < 2. Skip b[2]. j=3.
        # j=3, b[3]=1 < 2. Skip b[3]. j=4.
        # j=4, b[4]=1 < 2. Skip b[4]. j=5.
        # j=5 (==m). No more problems. extra_needed += 1 (for req=2). i=2.
        # i=2, req=3. j=5. No more problems. extra_needed += 1 (for req=3). i=3.
        # Total extra = 2. Correct.
        
        # Another trace:
        # a = [1, 2, 3], b = [1, 2, 2, 3, 3]
        # i=0, req=1. j=0, b[0]=1 >= 1. Match. j=1, i=1.
        # i=1, req=2. j=1, b[1]=2 >= 2. Match. j=2, i=2.
        # i=2, req=3. j=2, b[2]=2 < 3. Skip. j=3.
        # j=3, b[3]=3 >= 3. Match. j=4, i=3.
        # Done. extra=0. Correct.
        
        # This logic holds.
        
        pass

    # Implementation
    i = 0
    j = 0
    extra = 0
    
    while i < n:
        if j < m and b[j] < a[i]:
            j += 1
        elif j < m and b[j] >= a[i]:
            j += 1
            i += 1
        else:
            extra += 1
            i += 1
            
    print(extra)

if __name__ == '__main__':
    solve()