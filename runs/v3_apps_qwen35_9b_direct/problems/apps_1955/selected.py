import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    
    d = []
    idx = 2
    for _ in range(n):
        d.append(int(data[idx]))
        idx += 1
        
    a = []
    for _ in range(m):
        a.append(int(data[idx]))
        idx += 1
    
    # If total preparation days exceed n, it's impossible
    if sum(a) >= n:
        print(-1)
        return

    # Binary search for the minimum number of days
    # Range: [1, n]
    low = 1
    high = n
    ans = -1
    
    # Precompute suffix sums of preparation requirements to quickly check feasibility
    # suffix_prep[i] = sum of a[j] for j from i to m-1 (0-indexed subjects)
    # But we need to check if we can fit all exams in [0, limit-1]
    # Strategy: For a fixed 'limit' (number of days), we try to pass exams on the last possible day available in [0, limit-1] for each subject.
    # If we pass exam i on day 'day', we need 'a[i]' preparation days in [0, day-1].
    # To maximize chances, we should pass exams as late as possible within the window [0, limit-1].
    
    # Let's refine the check function:
    # Given a limit 'L' (days 0 to L-1):
    # 1. Identify all days in [0, L-1] where an exam can be taken.
    # 2. For each subject i, find the latest day in [0, L-1] where d[day] == i.
    #    If no such day exists, this limit is invalid.
    # 3. Sort these latest exam days in ascending order.
    # 4. Iterate through subjects. For subject i with exam day 'exam_day':
    #    - We need 'a[i]' preparation days in [0, exam_day - 1].
    #    - The days available for preparation are all days in [0, exam_day - 1] EXCEPT:
    #      - Days used for other exams (which are fixed to their latest possible days).
    #      - Days used for preparation for previous exams.
    #    - Actually, a simpler greedy approach for the check:
    #      Process days from L-1 down to 0.
    #      Keep track of how many preparation days are needed for each subject.
    #      If we encounter a day where an exam for subject 's' can be taken:
    #        If we still need to take exam 's' (i.e., we haven't scheduled it yet in this backward pass):
    #          We MUST take it here (since this is the latest possible day for 's' in [0, L-1]).
    #          We need 'a[s]' preparation days.
    #          We can use any free days in [0, current_day - 1] for preparation.
    #          But wait, if we process backwards, we don't know the future (earlier days) usage yet.
    #
    # Alternative Check Logic (Forward Greedy with Backward Validation):
    # For a fixed limit L:
    # 1. For each subject, find the latest day <= L-1 where the exam is available.
    #    If any subject has no such day, return False.
    # 2. Let's say we have a set of mandatory exam days: {day_1, day_2, ..., day_m} corresponding to subjects.
    #    Sort these days: t_1 < t_2 < ... < t_m.
    # 3. We need to assign preparation days.
    #    For exam at t_k (subject s_k), we need a[s_k] days in [0, t_k - 1].
    #    The days t_1, ..., t_k are occupied by exams.
    #    So available days in [0, t_k - 1] are (t_k) - k (since k days are taken by exams t_1...t_k).
    #    Wait, this is not quite right because preparation can happen on days that are NOT exam days.
    #    Total days in [0, t_k - 1] is t_k.
    #    Number of exam days in [0, t_k - 1] is k-1 (t_1...t_{k-1}).
    #    So free days in [0, t_k - 1] = t_k - (k-1).
    #    We need to fit a[s_k] preparation days for subject s_k in the free days of [0, t_k - 1] that are NOT used by s_1...s_{k-1}.
    #    This looks like we need to check if sum(a) fits, but specifically, for each prefix of sorted exam days, 
    #    the number of free days must be sufficient to cover the preparation for the exams scheduled up to that point?
    #    No, preparation for exam k can happen after exam j (j < k) is passed? No, preparation must be BEFORE the exam.
    #    So for exam at t_k, we need a[s_k] days in [0, t_k - 1] that are not exam days.
    #    The constraint is: For every k from 1 to m, the number of non-exam days in [0, t_k - 1] must be >= sum(a[s_1]...a[s_k])?
    #    No, that's too strong. We can interleave.
    #    Actually, the condition is: For each exam i scheduled at day t_i, we need a[i] days in [0, t_i-1] that are not exam days.
    #    Since we fixed the exam days to be the latest possible, the set of exam days is fixed.
    #    Let the sorted exam days be T = [t_1, t_2, ..., t_m].
    #    For each k, the number of available preparation slots in [0, t_k - 1] is (t_k) - (number of exams in [0, t_k - 1]).
    #    Number of exams in [0, t_k - 1] is k-1.
    #    So available slots = t_k - (k-1).
    #    We need to fit a[s_1] + ... + a[s_k] preparation days into the union of [0, t_1-1], [0, t_2-1], ...?
    #    No, preparation for s_k must be in [0, t_k-1]. Preparation for s_j (j<k) must be in [0, t_j-1].
    #    Since t_j < t_k, [0, t_j-1] is a subset of [0, t_k-1].
    #    The total preparation needed for the first k exams is sum(a[s_1]...a[s_k]).
    #    The total capacity for preparation for these k exams is the total number of non-exam days in [0, t_k - 1].
    #    Why? Because any non-exam day in [0, t_k - 1] can be used for any of the first k exams (since their deadlines are <= t_k).
    #    Wait, can a day in [t_j, t_k-1] be used for exam j? No, because exam j is at t_j, and prep must be before.
    #    So prep for exam j must be in [0, t_j-1].
    #    Prep for exam k must be in [0, t_k-1].
    #    The sets of valid prep days for different exams overlap.
    #    However, a single day can only be used for one purpose (one exam's prep or one exam itself).
    #    So, for the set of exams {s_1, ..., s_k} with deadlines {t_1, ..., t_k} (sorted by deadline):
    #    Total days required = sum(a[s_1]...a[s_k]) + k (for the exams themselves).
    #    These must fit into [0, t_k - 1] U {t_1, ..., t_k}.
    #    Actually, the exams themselves take up k days in [0, t_k].
    #    The preparation takes up sum(a) days in [0, t_k - 1].
    #    Total days needed in [0, t_k] is k + sum(a[s_1]...a[s_k]).
    #    But we only have t_k + 1 days in [0, t_k].
    #    So we need: k + sum(a[s_1]...a[s_k]) <= t_k + 1?
    #    Let's re-verify.
    #    Days in [0, t_k] is t_k + 1.
    #    We use k days for exams (t_1...t_k).
    #    We use sum(a) days for prep.
    #    All prep must be in [0, t_k - 1] for the respective exams.
    #    Since t_1 < t_2 < ... < t_k, the union of prep intervals is [0, t_k - 1].
    #    The exams occupy t_1, t_2, ..., t_k.
    #    So the number of available slots in [0, t_k - 1] is (t_k) - (k-1). (Total days t_k minus k-1 exam days before t_k).
    #    We need to fit sum(a[s_1]...a[s_k]) into these slots.
    #    So condition: sum(a[s_1]...a[s_k]) <= t_k - (k-1).
    #    Rearranging: sum(a[s_1]...a[s_k]) + k - 1 <= t_k.
    #    Or: sum(a[s_1]...a[s_k]) + k <= t_k + 1.
    #    This must hold for all k from 1 to m.
    #    Also, we need t_k <= L-1 for all k (which is guaranteed if we pick latest <= L-1).
    
    # Algorithm for check(L):
    # 1. Find latest day <= L-1 for each subject. If any missing, return False.
    # 2. Collect pairs (day, subject_index).
    # 3. Sort by day.
    # 4. Iterate k from 0 to m-1:
    #      current_day = sorted_days[k].day
    #      subject = sorted_days[k].subject
    #      needed = a[subject]
    #      current_sum += needed
    #      count_exams = k + 1
    #      if current_sum + count_exams > current_day + 1:
    #          return False
    # 5. return True

    def check(limit):
        # limit is the number of days considered (0 to limit-1)
        # Find latest day for each subject in [0, limit-1]
        last_day = [-1] * m
        for day in range(limit):
            subj = d[day]
            if subj != 0:
                last_day[subj] = day
        
        # Check if all subjects have a day
        for i in range(m):
            if last_day[i] == -1:
                return False
        
        # Sort by day
        events = []
        for i in range(m):
            events.append((last_day[i], i))
        events.sort(key=lambda x: x[0])
        
        current_prep_needed = 0
        for day, subj in events:
            current_prep_needed += a[subj]
            # Number of exams scheduled so far (including current)
            num_exams = events.index((day, subj)) + 1 # This is O(m) inside loop, optimize?
            # Actually, we can just use a counter.
            # But wait, events is sorted by day. The index in the sorted list is exactly the number of exams scheduled so far.
            # However, multiple exams can't be on the same day. The problem says "not allowed to pass more than one exam on any day".
            # So all days in 'events' are distinct.
            # So index + 1 is correct.
            
            # Condition: current_prep_needed + num_exams <= day + 1
            if current_prep_needed + (events.index((day, subj)) + 1) > day + 1:
                return False
        
        return True

    # Optimization: avoid index() in loop
    # We can just iterate with an index variable.
    
    def check_optimized(limit):
        last_day = [-1] * m
        for day in range(limit):
            subj = d[day]
            if subj != 0:
                last_day[subj] = day
        
        for i in range(m):
            if last_day[i] == -1:
                return False
        
        events = []
        for i in range(m):
            events.append((last_day[i], i))
        events.sort(key=lambda x: x[0])
        
        current_prep_needed = 0
        for k, (day, subj) in enumerate(events):
            current_prep_needed += a[subj]
            # k is 0-based index, so number of exams is k+1
            if current_prep_needed + (k + 1) > day + 1:
                return False
        return True

    low = 1
    high = n
    ans = -1
    
    while low <= high:
        mid = (low + high) // 2
        if check_optimized(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
            
    print(ans)

if __name__ == '__main__':
    solve()