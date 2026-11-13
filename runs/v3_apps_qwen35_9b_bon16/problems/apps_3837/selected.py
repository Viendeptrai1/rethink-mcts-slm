import sys

# Increase recursion depth just in case, though we will use an iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
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

    # Combine student abilities and costs
    # Each student is (ability, cost, original_index)
    students = []
    for i in range(n):
        students.append((b[i], c[i], i + 1))
    
    # Sort students by ability descending
    students.sort(key=lambda x: x[0], reverse=True)
    
    # Sort bugs by complexity descending
    # We need to keep track of original indices to output the answer correctly
    bugs_with_idx = []
    for i in range(m):
        bugs_with_idx.append((a[i], i))
    
    bugs_with_idx.sort(key=lambda x: x[0], reverse=True)
    
    # Check if even the strongest student can handle the most complex bug
    if not students:
        print("NO")
        return
    
    if students[0][0] < bugs_with_idx[0][0]:
        print("NO")
        return

    # Binary search for the minimum number of days (k)
    # Range of k: [1, m]
    low = 1
    high = m
    ans_days = m + 1
    
    # Helper to check if a given number of days is feasible
    def can_solve(k_days):
        # We need to assign bugs to students such that:
        # 1. Each bug is assigned to a student with ability >= bug complexity
        # 2. Each student can fix at most k_days bugs (since they work 1 bug/day and have k_days days)
        # 3. Total cost <= s
        
        # Strategy:
        # Since bugs are sorted by complexity descending and students by ability descending:
        # We process bugs from hardest to easiest.
        # For the current bug (complexity X), we can only use students with ability >= X.
        # Among all available students who can handle this bug (and thus all easier bugs),
        # we should pick those with the lowest cost to minimize total cost.
        # However, we also have a constraint on the count per student (k_days).
        
        # Let's maintain a pool of "available" students who can handle the current bug.
        # Since we iterate bugs from hardest to easiest, the set of eligible students grows (or stays same).
        # Specifically, if a student has ability >= current_bug_complexity, they are eligible.
        # Because we sort bugs descending, once a student becomes eligible, they stay eligible for all subsequent (easier) bugs.
        
        # We need a data structure to:
        # 1. Add students as they become eligible.
        # 2. Select the student with the minimum cost who still has capacity (< k_days).
        
        # We can use a min-heap for the costs of eligible students who have capacity.
        # When we pick a student, we decrement their capacity.
        # However, simply removing from a heap when capacity drops is tricky.
        # Alternative: Keep all eligible students in a structure.
        # Since we only care about the cheapest available student, we can maintain a min-heap of (cost, student_index, remaining_capacity).
        # But when capacity reaches 0, we need to remove them.
        # Or, we can just mark them as full. But a heap doesn't support efficient removal of arbitrary elements.
        
        # Better approach:
        # We iterate bugs. We add all newly eligible students to a min-heap based on cost.
        # The heap stores (cost, student_index).
        # We also need to track how many bugs each student has already been assigned.
        # When we need to assign a bug, we peek at the heap.
        # If the top student has reached k_days assignments, we pop them (they are full) and check the next one.
        # If the heap becomes empty, then it's impossible.
        
        # Wait, there's a catch: A student might be added to the heap, but later we find they are full.
        # Standard lazy removal: When popping from heap, if the student is already full (assigned == k_days), discard and pop again.
        
        # Let's implement this.
        
        import heapq
        
        # Min-heap: (cost, student_index)
        eligible_heap = []
        
        # Track assignments per student
        # student_assignments[i] = number of bugs assigned to student i (1-based index)
        # Since n can be 10^5, an array is fine.
        student_assignments = [0] * (n + 1)
        
        total_cost = 0
        idx_student = 0 # Pointer to students array (sorted by ability desc)
        
        # We also need to know the ability of the student to ensure they can handle the current bug?
        # Actually, since we add students to the heap only when their ability >= current bug complexity,
        # we don't need to check ability again.
        # But wait: The students array is sorted by ability descending.
        # Bugs are sorted by complexity descending.
        # As we move to easier bugs, more students become eligible.
        # Specifically, while students[idx_student].ability >= current_bug_complexity:
        #    Add this student to the heap.
        #    idx_student += 1
        
        # This logic holds: if a student can handle bug j (complexity A), and bug j+1 has complexity A' <= A,
        # then that student can also handle bug j+1. So once eligible, always eligible.
        
        # Let's refine the loop.
        # bugs_with_idx is sorted desc by complexity.
        # students is sorted desc by ability.
        
        for bug_complexity, original_bug_idx in bugs_with_idx:
            # Add all students who can handle this bug
            while idx_student < n and students[idx_student][0] >= bug_complexity:
                # Push to heap: (cost, student_original_index)
                # Note: student_original_index is 1-based
                heapq.heappush(eligible_heap, (students[idx_student][1], students[idx_student][2]))
                idx_student += 1
            
            if not eligible_heap:
                return False
            
            # Get the cheapest student who has capacity
            cost, student_idx = eligible_heap[0]
            
            # Check if this student is already full (assigned k_days bugs)
            # Since we might have added a full student to the heap earlier and haven't popped them yet,
            # we must check before assigning.
            # However, we don't remove full students immediately. We only check at the top.
            # If the top is full, we pop and check the next.
            
            while student_assignments[student_idx] == k_days:
                heapq.heappop(eligible_heap)
                if not eligible_heap:
                    return False
                cost, student_idx = eligible_heap[0]
            
            # Assign the bug
            student_assignments[student_idx] += 1
            total_cost += cost
            
            # We don't remove from heap yet because they might still have capacity.
            # But if they become full, we will pop them next time they come to the top.
            # Is it possible that a full student is NOT at the top?
            # Yes, if there is a cheaper student who is also full? No, if a student is full, they are useless.
            # If there is a cheaper student with capacity, they will be at the top.
            # If the cheapest student is full, we pop.
            # If the second cheapest is full, we pop, etc.
            # So the logic "while top is full, pop" works correctly because we always want the cheapest with capacity.
            # Wait, what if the cheapest is full, we pop, but the next cheapest is also full? We loop.
            # What if the cheapest is NOT full? We use them. We do NOT pop them.
            # Later, if they become full, they will eventually reach the top again (since heap order is static based on cost).
            # When they reach the top, we will check and pop them.
            # This is correct.
        
        return total_cost <= s

    # Binary Search
    while low <= high:
        mid = (low + high) // 2
        if can_solve(mid):
            ans_days = mid
            high = mid - 1
        else:
            low = mid + 1
    
    if ans_days == m + 1:
        print("NO")
    else:
        print("YES")
        
        # Re-run the assignment logic for ans_days to build the result
        import heapq
        
        students_sorted = sorted([(b[i], c[i], i+1) for i in range(n)], key=lambda x: x[0], reverse=True)
        bugs_sorted = sorted([(a[i], i) for i in range(m)], key=lambda x: x[0], reverse=True)
        
        eligible_heap = []
        student_assignments = [0] * (n + 1)
        idx_student = 0
        
        assignment_map = {} # original_bug_idx -> student_idx
        
        for bug_complexity, original_bug_idx in bugs_sorted:
            while idx_student < n and students_sorted[idx_student][0] >= bug_complexity:
                heapq.heappush(eligible_heap, (students_sorted[idx_student][1], students_sorted[idx_student][2]))
                idx_student += 1
            
            if not eligible_heap:
                # Should not happen if can_solve returned True
                break
                
            cost, student_idx = eligible_heap[0]
            
            while student_assignments[student_idx] == ans_days:
                heapq.heappop(eligible_heap)
                if not eligible_heap:
                    break
                cost, student_idx = eligible_heap[0]
            
            # We assume we found one because can_solve passed
            student_assignments[student_idx] += 1
            assignment_map[original_bug_idx] = student_idx
        
        # Output the assignments in the original order
        result = [assignment_map[i] for i in range(m)]
        print(*(result))

if __name__ == '__main__':
    solve()