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

    # Store student info as (ability, cost, original_index)
    students = []
    for i in range(n):
        students.append((b[i], c[i], i + 1))
    
    # Sort students by ability descending
    students.sort(key=lambda x: x[0], reverse=True)
    
    # Sort bugs by complexity descending
    bugs = []
    for i in range(m):
        bugs.append((a[i], i + 1))
    bugs.sort(key=lambda x: x[0], reverse=True)

    # Binary search for the minimum number of days
    low = 1
    high = m
    ans_days = m + 1
    best_assignment = None

    while low <= high:
        mid = (low + high) // 2
        
        # Check if it's possible to fix all bugs in 'mid' days with cost <= s
        # Greedy strategy:
        # 1. Process bugs from hardest to easiest.
        # 2. For the current hardest bug, we need a student with ability >= bug_complexity.
        # 3. Among available students (who can handle this bug), we should pick the one with the minimum cost.
        # 4. However, we have a constraint of 'mid' days. This means each student can take at most 'mid' bugs.
        # 5. Since bugs are processed hardest first, if we assign a student to a hard bug, they are "busy" for that day.
        #    But since we can parallelize, the constraint is simply: total bugs assigned to any student <= mid.
        #    Actually, the problem says "no student can work on a few bugs in one day". 
        #    So if a student takes k bugs, it takes k days. We need max(k) <= mid.
        
        # Algorithm for check(days):
        # We iterate bugs from hardest to easiest.
        # We maintain a pool of students who can handle the current bug (ability >= current_bug_complexity).
        # Since bugs are sorted descending, once a student qualifies for bug i, they qualify for all previous (harder) bugs? 
        # No, ability >= bug_complexity. If bug_complexity decreases, the set of qualifying students grows (or stays same).
        # So as we go from hardest to easiest bugs, more students become eligible.
        # We want to assign the current bug to an eligible student who has the minimum cost, 
        # but also hasn't reached the 'days' limit.
        # To optimize, we can use a min-heap for costs of eligible students.
        
        # However, we also need to track how many bugs each student has taken.
        # Since we process bugs hardest to easiest, and we want to minimize cost, 
        # we should pick the cheapest eligible student who still has capacity.
        # If the cheapest eligible student is full, we pick the next cheapest, etc.
        # If no student has capacity, then this 'days' is not feasible.
        
        # Optimization: 
        # Instead of simulating day by day, we can think:
        # We have 'days' slots per student. Total capacity = n * days.
        # But we need to distribute the load.
        # Greedy approach:
        # Iterate bugs from hardest to easiest.
        # Maintain a set of students who can handle the current bug (ability >= current).
        # Since bugs are sorted descending, we can add students to our candidate pool as their ability becomes sufficient.
        # Specifically, if current bug complexity is X, any student with ability >= X is eligible.
        # Since we go descending, we can maintain a pointer in the sorted students list.
        # Add all students with ability >= current_bug_complexity to a min-heap of (cost, student_index).
        # But wait, a student might be added multiple times? No, each student is added once when they become eligible.
        # However, we need to know if a student is "full".
        # If the cheapest student in the heap is full, we pop them and look for the next cheapest.
        # If we pop a student and they are full, we discard them? 
        # Yes, because they can't take more bugs.
        # But what if a cheaper student becomes available later? 
        # No, we are processing bugs hardest to easiest. The set of eligible students only grows.
        # So the pool of eligible students is cumulative.
        # The issue is: if the current cheapest eligible student is full, can we use a more expensive one? Yes.
        # Can we use a student who was eligible for a harder bug but we didn't use them? 
        # Yes, they are still in the pool.
        
        # Refined Check(days):
        # 1. Sort bugs descending.
        # 2. Sort students descending by ability.
        # 3. Use a min-heap for costs of eligible students. The heap will store (cost, student_index).
        #    We also need to track how many bugs each student has taken. Let's use an array `count`.
        # 4. Iterate through bugs (hardest to easiest):
        #    a. Add all students with ability >= current_bug_complexity to the heap.
        #       Since students are sorted descending by ability, we can maintain an index `student_ptr`.
        #       While `student_ptr < n` and `students[student_ptr].ability >= current_bug_complexity`:
        #           Push (students[student_ptr].cost, students[student_ptr].index) to heap.
        #           Increment `student_ptr`.
        #    b. If heap is empty, return False (no one can fix this bug).
        #    c. Pop the student with minimum cost from the heap.
        #    d. If this student has already taken `days` bugs, they are full.
        #       We must try the next cheapest.
        #       So we pop again. If the next one is also full, pop again.
        #       If we exhaust the heap, return False.
        #    e. Assign this bug to the popped student. Increment their count.
        #       Add the cost to total.
        #       If total > s, return False.
        #    f. Push the student back into the heap? 
        #       Wait, if they are not full, they can take another bug.
        #       But we just popped them. If we push them back, they will be at the top again (since cost is same).
        #       This is correct.
        #       However, if they are full, we discard them (do not push back).
        
        # One detail: The heap stores (cost, index). If costs are equal, index doesn't matter.
        # But we need to ensure we don't re-add a student who is full.
        
        # Let's implement this check.
        
        possible = True
        current_cost = 0
        student_counts = [0] * (n + 1) # 1-based index
        student_ptr = 0
        heap = [] # min-heap of (cost, index)
        
        # We need to map back to original student data
        # students list is sorted by ability. We need to access cost and index.
        # Let's create a lookup or just use the tuple.
        # Actually, the heap needs (cost, original_index).
        # We can store (cost, original_index) in the heap.
        
        for bug_complexity, bug_idx in bugs:
            # Add eligible students
            while student_ptr < n and students[student_ptr][0] >= bug_complexity:
                # students[student_ptr] is (ability, cost, original_index)
                cost = students[student_ptr][1]
                idx = students[student_ptr][2]
                heapq.heappush(heap, (cost, idx))
                student_ptr += 1
            
            if not heap:
                possible = False
                break
            
            # Find a student with capacity
            while heap:
                cost, idx = heapq.heappop(heap)
                if student_counts[idx] < days:
                    # Assign bug
                    student_counts[idx] += 1
                    current_cost += cost
                    if current_cost > s:
                        possible = False
                        break
                    # Push back if not full
                    heapq.heappush(heap, (cost, idx))
                    break
                # else: student is full, discard and try next
            
            if not possible:
                break
        
        if possible:
            ans_days = mid
            # We need to reconstruct the assignment for the optimal answer
            # But wait, the binary search only tells us the min days.
            # We need to run the check one more time with ans_days to get the actual assignment.
            # And we need to store the assignment.
            break
        else:
            low = mid + 1

    if ans_days == m + 1:
        print("NO")
        return

    # Re-run the assignment logic with ans_days to get the specific mapping
    # We need to output the student index for each bug in the original order.
    # So we need to store the assignment.
    
    student_counts = [0] * (n + 1)
    student_ptr = 0
    heap = []
    assignment = [0] * (m + 1) # 1-based
    
    # Reset student_ptr and heap
    student_ptr = 0
    heap = []
    current_cost = 0
    
    for bug_complexity, bug_idx in bugs:
        while student_ptr < n and students[student_ptr][0] >= bug_complexity:
            cost = students[student_ptr][1]
            idx = students[student_ptr][2]
            heapq.heappush(heap, (cost, idx))
            student_ptr += 1
        
        if not heap:
            # Should not happen if ans_days is valid
            print("NO")
            return

        while heap:
            cost, idx = heapq.heappop(heap)
            if student_counts[idx] < ans_days:
                student_counts[idx] += 1
                current_cost += cost
                assignment[bug_idx] = idx
                heapq.heappush(heap, (cost, idx))
                break
            # else discard

    print("YES")
    # Output assignment for bugs 1 to m
    print(*(assignment[1:]))

# Import heapq inside or outside? Outside is better.
import heapq

if __name__ == '__main__':
    solve()