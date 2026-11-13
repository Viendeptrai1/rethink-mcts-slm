import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    
    d = []
    for _ in range(n):
        d.append(int(data[idx])); idx += 1
        
    a = []
    for _ in range(m):
        a.append(int(data[idx])); idx += 1
        
    # Check if total days needed is feasible even without gaps
    if sum(a) + m > n:
        print(-1)
        return

    # Binary search for the minimum number of days
    def check(limit_days):
        # We need to pass all exams by 'limit_days'
        # Iterate backwards from 'limit_days' to 1
        # Keep track of required preparation days for each subject
        # If we encounter an exam day for subject s within the window, we can take it
        # if we have already prepared enough. If not, we must prepare now (if possible).
        
        required = [0] * (m + 1)
        # We simulate the process backwards from 'limit_days' down to 1
        # Actually, we can just iterate once backwards and greedily assign preparation days.
        
        # However, the greedy strategy "take exam as late as possible" implies:
        # Iterate i from limit_days down to 1:
        #   If d[i-1] != 0 and required[d[i-1]] == 0:
        #      This is the last chance to take this exam (since we go backwards).
        #      Mark it as taken. We need to reserve 'a[d[i-1]-1]' days BEFORE this day for prep.
        #      But since we are going backwards, we can't "reserve" future days easily in a simple loop.
        #      
        # Better approach:
        # 1. Identify the last possible day to take each exam within [1, limit_days].
        #    If an exam type doesn't appear, impossible.
        #    If multiple days have the same exam, pick the largest index.
        # 2. Sort these exams by their scheduled day (ascending).
        # 3. Iterate through the sorted exams. For each exam, we schedule it on its chosen day.
        #    We need to ensure there are enough free days BEFORE this day to prepare.
        #    The days used for preparation can be any day in [1, exam_day - 1] that is not used for another exam or prep.
        #    Since we process in order of exam days, we can maintain a count of available days.
        #    Actually, a simpler greedy:
        #    Let's collect the exams to be taken: (exam_subject, day_index).
        #    Sort by day_index.
        #    Maintain a set of busy days (exam days).
        #    For each exam (sub, day) in sorted order:
        #      We need 'a[sub]' preparation days.
        #      These days must be strictly before 'day'.
        #      We can use any day < 'day' that is not an exam day and not already used for prep.
        #      To maximize chances, we should greedily use the latest possible days before 'day' for prep?
        #      Wait, if we use the latest possible days, we might conflict with an earlier exam's prep needs?
        #      Actually, the standard greedy for this problem (going backwards) is:
        #      Iterate i from limit_days down to 1.
        #      Keep track of which subjects we have scheduled to take (by finding their latest occurrence <= i).
        #      If we find an exam day for subject S and we haven't scheduled S yet:
        #         We MUST take S on this day (because it's the latest chance).
        #         We need 'a[S]' days of prep.
        #         We count how many days in range [1, i-1] are currently "free" (not exam days).
        #         But we are building the schedule backwards.
        #      
        # Correct Logic (Backwards Greedy):
        # 1. Find the last occurrence of each subject j in range [1, limit_days].
        #    If any subject is missing, return False.
        # 2. Let's create a list of events: for each subject j, the event is (last_day[j], j).
        # 3. Sort these events by day ascending.
        # 4. Iterate through the sorted events. Let current exam be for subject j at day D.
        #    We need 'a[j]' preparation days.
        #    The days available for preparation are all days in [1, D-1] EXCEPT:
        #      - Days where we schedule other exams (which we will know about eventually? No, we process in order).
        #      - Days already used for preparation for previous exams.
        #    
        #    Actually, processing in ascending order of exam days is tricky because prep for later exams can use days that are earlier than the current exam but might be needed for earlier exams? No, prep must be before the exam.
        #    Prep for exam at D_j must be in [1, D_j-1].
        #    If we process exams in increasing order of D_j:
        #      Current exam at D_j needs a[j] days from [1, D_j-1].
        #      Some of these days might be occupied by previous exams (D_k < D_j).
        #      The remaining days can be used for prep.
        #      We also need to account for the fact that we can interleave prep.
        #      
        #    Let's re-evaluate the "Backwards" approach which is standard for this problem.
        #    Algorithm:
        #      1. Identify the latest day <= limit_days for each subject. If any missing -> False.
        #      2. Create a list of these exams: (day, subject).
        #      3. Sort this list by day ascending.
        #      4. Iterate through the list. Maintain a variable `total_prep_needed`? No.
        #         Maintain a set of `used_days` (exam days).
        #         Also, we need to track how many days are "available" for prep before the current exam day.
        #         Actually, the constraint is: Sum of (a[j] for exams up to i) + Count of exams up to i <= D_i?
        #         Not exactly, because the prep days don't have to be contiguous and can be shared? No, prep days are distinct.
        #         Total days consumed = (Number of exams) + (Sum of prep days).
        #         But the constraint is temporal: for the k-th exam in chronological order (at day T_k),
        #         we need T_k >= k + sum(a[exam 1]...a[exam k]).
        #         Why? Because we have k exams to take at days T_1, T_2, ..., T_k.
        #         And we need sum(a) days of prep. All these must happen before T_k.
        #         So the time required up to T_k is k (for the exams themselves) + sum(a) (for prep).
        #         Since all these activities happen before T_k, we must have T_k >= k + sum(a).
        #         Is this sufficient? Yes, because if T_k >= k + sum(a), we can fit k exams and sum(a) prep days in [1, T_k].
        #         Specifically, we can schedule the k exams at T_1...T_k and fill the rest of [1, T_k] with prep.
        #         Wait, the prep for exam i must be BEFORE T_i.
        #         Does T_k >= k + sum_{j=1 to k} a_j guarantee that prep for exam k is before T_k?
        #         Yes, because the total volume of work (k exams + sum prep) fits in T_k days.
        #         And since T_1 < T_2 < ... < T_k, the prep for earlier exams can be done in the gaps before T_2, etc.
        #         Actually, the condition is slightly stricter:
        #         For every prefix of exams (sorted by day), the total required days must fit in the day of the last exam in the prefix.
        #         Let the exams we chose to take be at days t_1 < t_2 < ... < t_m.
        #         Condition: For all k from 1 to m: t_k >= k + sum_{j=1}^k a_{subject(t_j)}.
        #         If this holds for all k, then it's possible.
        
        # Implementation of check(limit_days):
        # 1. Find last occurrence of each subject in d[0...limit_days-1].
        # 2. If any subject missing, return False.
        # 3. Collect pairs (day_index, subject_idx) for the last occurrences.
        # 4. Sort by day_index.
        # 5. Iterate and check the condition.
        
        present = [False] * m
        last_occurrence = {}
        # d is 0-indexed, day numbers 1 to n
        # We only care about days 1 to limit_days
        for day in range(1, limit_days + 1):
            subj = d[day-1]
            if subj != 0:
                last_occurrence[subj] = day
        
        if len(last_occurrence) != m:
            return False
            
        exams = []
        for subj in range(1, m+1):
            exams.append((last_occurrence[subj], subj))
        
        exams.sort(key=lambda x: x[0])
        
        current_exam_count = 0
        current_prep_sum = 0
        
        for day, subj in exams:
            current_exam_count += 1
            current_prep_sum += a[subj-1]
            # We need current_exam_count days for the exams themselves (the days they are taken)
            # plus current_prep_sum days for preparation.
            # All these must be within [1, day].
            # So: day >= current_exam_count + current_prep_sum
            if day < current_exam_count + current_prep_sum:
                return False
                
        return True

    left = 1
    right = n
    ans = -1
    
    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1
            
    print(ans)

if __name__ == '__main__':
    solve()