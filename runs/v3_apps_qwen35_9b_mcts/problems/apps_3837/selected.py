import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)

    try:
        n = int(next(iterator))
        m = int(next(iterator))
        s = int(next(iterator))
        
        a = []
        for _ in range(m):
            a.append(int(next(iterator)))
            
        b = []
        for _ in range(n):
            b.append(int(next(iterator)))
            
        c = []
        for _ in range(n):
            c.append(int(next(iterator)))
    except StopIteration:
        return

    # Sort bugs by complexity descending
    bugs = sorted([(a[i], i) for i in range(m)], key=lambda x: x[0], reverse=True)
    
    # Sort students by ability descending, then by cost ascending (to prefer cheaper among capable)
    # We need to pick students greedily based on ability.
    # Strategy: For a fixed number of days k, we can process bugs in groups of k.
    # The hardest k bugs must be handled by students with ability >= max_complexity_of_those_k_bugs.
    # To minimize cost, for each group, we should pick the cheapest available student who can handle the hardest bug in that group.
    # Since bugs are sorted descending, the i-th group (0-indexed) of k bugs starts at index i*k and ends at (i+1)*k - 1.
    # The hardest bug in this group is at index i*k.
    # We need a student with ability >= bugs[i*k].complexity.
    # Among all such students, we want the one with minimum cost.
    # However, a student can only be used once per day. So in k days, a student can fix k bugs.
    # But the constraint is simpler: In day 1, we assign k bugs to k different students.
    # In day 2, we assign the next k bugs to k different students (can reuse students from day 1).
    # Actually, the problem says "no student can work on a few bugs in one day".
    # So if we have k days, we can distribute the m bugs into k batches of size at most k.
    # To minimize days, we want to maximize the batch size, which is k.
    # So we divide m bugs into ceil(m/k) batches.
    # Batch 0: bugs[0...k-1], hardest is bugs[0]. Need student with ability >= bugs[0].
    # Batch 1: bugs[k...2k-1], hardest is bugs[k]. Need student with ability >= bugs[k].
    # ...
    # Batch j: bugs[j*k ... min((j+1)*k, m)-1], hardest is bugs[j*k].
    # For each batch, we need to select a student. The cost is c[student_id].
    # The total cost is sum of costs of selected students for all batches.
    # Wait, can we reuse a student across batches? Yes. "different students can work simultaneously" refers to parallelism within a day.
    # Across days, a student can work again.
    # So for each batch, we independently select the cheapest student capable of handling the hardest bug in that batch.
    # BUT, there is a catch. If we select the same student for multiple batches, does it matter?
    # No, because they work on different days.
    # So the cost for a fixed k is sum over j=0 to ceil(m/k)-1 of (min cost of student with ability >= bugs[j*k].complexity).
    # We need to find the minimum k such that total cost <= s.
    
    # Precompute students sorted by ability descending.
    # We also need to quickly query: given a complexity X, what is the minimum cost among students with ability >= X?
    # Since bugs are sorted descending, the required ability for batch j is bugs[j*k].complexity.
    # As j increases, bugs[j*k].complexity decreases (or stays same).
    # So the set of eligible students grows (or stays same) as j increases.
    # We can maintain a running minimum cost.
    
    # Let's create a list of students sorted by ability descending.
    # students_info = [(ability, cost, original_index), ...]
    students_info = []
    for i in range(n):
        students_info.append((b[i], c[i], i + 1))
    students_info.sort(key=lambda x: x[0], reverse=True)
    
    # Precompute prefix minimums? 
    # Actually, since the required ability threshold decreases as we go through batches,
    # we can iterate through the sorted students and maintain the best cost seen so far for abilities >= current threshold.
    # However, the thresholds are specific values from the bugs array.
    # Let's just collect all unique ability thresholds from the bugs (specifically the start of each batch).
    # But simpler: Just iterate.
    
    # To optimize, let's precompute an array `min_cost_for_ability`?
    # The abilities can be up to 10^9, so we can't use an array.
    # But we have at most N students and M bugs.
    # We can sort the bugs' start complexities.
    # Actually, the sequence of required abilities for batches is: bugs[0], bugs[k], bugs[2k]...
    # This sequence is non-increasing.
    # We can iterate through the sorted students and keep track of the minimum cost encountered so far.
    # For a specific batch requiring ability A, we need min cost among students with ability >= A.
    # Since students are sorted by ability descending, we can maintain a pointer to the first student with ability >= A.
    # All students from index 0 to that pointer are eligible. We need the min cost in that range.
    # We can precompute prefix minimums of costs for the sorted students list.
    
    sorted_students = sorted(students_info, key=lambda x: x[0], reverse=True)
    # prefix_min_cost[i] = min(cost of sorted_students[0]...sorted_students[i])
    prefix_min_cost = [0] * n
    current_min = float('inf')
    for i in range(n):
        if sorted_students[i][1] < current_min:
            current_min = sorted_students[i][1]
        prefix_min_cost[i] = current_min
    
    # Function to check if k days are sufficient
    def check(k):
        if k == 0:
            return False
        total_cost = 0
        # Number of batches
        num_batches = (m + k - 1) // k
        
        # We need to process batches. The hardest bug in batch j is at index j*k in the sorted bugs list.
        # Let's iterate j from 0 to num_batches - 1.
        # For each batch, required ability = bugs[j*k].complexity.
        # We need min cost among students with ability >= required_ability.
        
        # Since required_ability is non-increasing as j increases, the set of eligible students expands.
        # We can maintain a pointer in sorted_students.
        ptr = 0
        for j in range(num_batches):
            req_ability = bugs[j*k][0]
            
            # Advance ptr while students[ptr].ability < req_ability? 
            # No, we need students with ability >= req_ability.
            # Since sorted_students is descending, we need to include all students from 0 up to some index where ability >= req_ability.
            # Actually, as req_ability decreases, the cutoff index moves to the right (more students become eligible).
            # So we advance ptr while sorted_students[ptr].ability >= req_ability.
            # Wait, if sorted_students is descending:
            # [10, 9, 8, 5, 3]
            # req = 8. Eligible: 10, 9, 8. Indices 0, 1, 2.
            # req = 5. Eligible: 10, 9, 8, 5. Indices 0, 1, 2, 3.
            # So yes, we advance ptr as long as sorted_students[ptr].ability >= req_ability.
            
            while ptr < n and sorted_students[ptr][0] >= req_ability:
                ptr += 1
            # Now eligible students are 0 to ptr-1.
            # The min cost is prefix_min_cost[ptr-1].
            if ptr == 0:
                return False # No student capable
            cost = prefix_min_cost[ptr-1]
            total_cost += cost
            if total_cost > s:
                return False
        return True

    # Binary search for minimum k
    low = 1
    high = m
    ans_k = -1
    
    # First check if even m days is possible (though check(m) should cover it)
    # Actually, if check(m) fails, then impossible.
    if not check(m):
        print("NO")
        return

    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans_k = mid
            high = mid - 1
        else:
            low = mid + 1
            
    if ans_k == -1:
        print("NO")
        return

    # Reconstruct the solution for ans_k
    k = ans_k
    num_batches = (m + k - 1) // k
    result = [0] * m
    
    ptr = 0
    for j in range(num_batches):
        start_idx = j * k
        end_idx = min((j + 1) * k, m)
        req_ability = bugs[start_idx][0]
        
        # Find eligible students
        while ptr < n and sorted_students[ptr][0] >= req_ability:
            ptr += 1
        
        # Best student is the one with min cost in 0..ptr-1
        # We need to pick one student. Which one? Any with min cost.
        # To be deterministic and simple, pick the first one in sorted_students that has the min cost.
        # But we need to output the original index.
        # Let's find the student index.
        best_student_idx = -1
        min_c = float('inf')
        for i in range(ptr):
            if sorted_students[i][1] < min_c:
                min_c = sorted_students[i][1]
                best_student_idx = sorted_students[i][2]
        
        # Assign this student to all bugs in this batch
        for idx in range(start_idx, end_idx):
            result[bugs[idx][1]] = best_student_idx
            
    print("YES")
    print(*(result))

if __name__ == '__main__':
    solve()