import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    exams = []
    for i in range(m):
        s = int(next(iterator))
        d = int(next(iterator))
        c = int(next(iterator))
        exams.append({'id': i + 1, 's': s, 'd': d, 'c': c})
    
    # Schedule array: 0 = rest, i = prepare for exam i, m+1 = take exam
    schedule = [0] * (n + 1)  # 1-based indexing for days
    
    # Mark exam days first
    exam_day_map = {}
    for i in range(m):
        exam_day_map[exams[i]['d']] = exams[i]['id']
        schedule[exams[i]['d']] = m + 1
    
    # Sort exams by their exam day (deadline)
    exams_sorted = sorted(exams, key=lambda x: x['d'])
    
    # Track how many days prepared for each exam
    prepared = [0] * m
    
    # Greedy approach: iterate day by day
    # If day is an exam day, we must take the exam.
    # If day is within preparation window for some exams, we can prepare.
    # To maximize flexibility, we should prioritize exams that have the nearest deadline
    # and haven't been fully prepared yet.
    
    # However, a simpler greedy strategy works here:
    # Iterate through days 1 to n.
    # If it's an exam day, skip (already marked).
    # If not an exam day, check which exams can be prepared on this day.
    # An exam i can be prepared on day j if:
    #   exams[i]['s'] <= j < exams[i]['d']
    #   and prepared[i] < exams[i]['c']
    # Among all available exams, pick the one with the smallest 'd' (earliest deadline).
    # If multiple have same deadline, any is fine.
    
    # Actually, we need to be careful. The standard solution for this problem is:
    # Sort exams by deadline. Then iterate days. On each non-exam day, if there are exams
    # that need preparation and are currently available (s_i <= day < d_i),
    # assign preparation to the exam with the earliest deadline among those available.
    
    # Let's refine the loop:
    # We can't just pick any exam. We must ensure we don't miss the deadline.
    # The optimal greedy strategy:
    # 1. Identify all exams that are "active" on the current day (s_i <= day < d_i).
    # 2. Among active exams that still need preparation, pick the one with the smallest d_i.
    # 3. If no such exam exists, rest.
    # 4. If an exam has a deadline on the current day (day == d_i), that's impossible for preparation,
    #    but our loop handles day < d_i, so if we reach day == d_i, we skip preparation logic.
    
    # Wait, the constraint is strictly day < d_i. So on day d_i, we CANNOT prepare.
    # So on day d_i, we MUST take the exam. Our schedule already marks it.
    
    # Algorithm:
    # For day from 1 to n:
    #   If day is an exam day: continue (already set to m+1)
    #   Else:
    #     Find all exams i such that s_i <= day < d_i and prepared[i] < c_i.
    #     If list is empty: schedule[day] = 0
    #     Else: pick exam with smallest d_i. If tie, any.
    #           schedule[day] = exam_id
    #           prepared[exam_idx] += 1
    
    # After filling, check if all exams are fully prepared.
    
    final_schedule = [0] * (n + 1)
    
    # Re-mark exam days in final_schedule
    for i in range(m):
        final_schedule[exams[i]['d']] = m + 1
    
    prepared = [0] * m
    
    for day in range(1, n + 1):
        if final_schedule[day] != 0:
            continue # It's an exam day or we didn't set it (default 0)
        
        # Find candidates
        candidates = []
        for idx in range(m):
            if prepared[idx] < exams[idx]['c']:
                if exams[idx]['s'] <= day < exams[idx]['d']:
                    candidates.append((exams[idx]['d'], idx))
        
        if not candidates:
            continue
        
        # Sort candidates by deadline
        candidates.sort(key=lambda x: x[0])
        
        # Pick the first one (earliest deadline)
        best_idx = candidates[0][1]
        final_schedule[day] = exams[best_idx]['id']
        prepared[best_idx] += 1
    
    # Verify
    for idx in range(m):
        if prepared[idx] < exams[idx]['c']:
            print("-1")
            return
    
    # Output result
    # Convert 1-based schedule to 0-based list for printing days 1..n
    result = []
    for day in range(1, n + 1):
        val = final_schedule[day]
        if val == 0:
            result.append("0")
        elif val == m + 1:
            result.append(str(val))
        else:
            result.append(str(val))
    
    print(" ".join(result))

if __name__ == "__main__":
    solve()