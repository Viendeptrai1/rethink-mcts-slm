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
    
    # If total preparation days exceed available days, impossible
    if sum(a) >= n:
        print(-1)
        return

    # Check function for binary search
    def check(k):
        # We need to pass all m exams within first k days
        # Iterate backwards from day k to 1
        # Keep track of which exams are already passed
        passed = [False] * m
        # Days needed for each exam
        needed = a[:]
        
        # We will simulate backwards
        # On day i (1-based), if d[i-1] != 0, we can potentially pass exam d[i-1]
        # If we haven't passed it yet, and we have enough days before this to prepare, we do it.
        
        # Actually, the greedy strategy backwards:
        # For each exam i, we must pass it on the latest possible day <= k where d[day] == i.
        # But we can only pass it if we have enough free days before that day to prepare.
        # However, since we can interleave, the standard greedy approach is:
        # Iterate days from k down to 1.
        # If day has an exam type t != 0:
        #   If we haven't passed exam t yet:
        #     We MUST pass it on this day (because this is the latest opportunity).
        #     Mark exam t as passed.
        #     Add needed[t] to our "preparation needed" counter.
        #   Else:
        #     This day is free for preparation (since we don't need to pass exam t anymore).
        # If day is 0:
        #   This day is free for preparation.
        
        # Wait, the logic above is slightly flawed. 
        # Correct logic:
        # We iterate backwards. We maintain a count of "days needed for preparation" for exams not yet passed.
        # When we encounter a day with exam type t:
        #   If exam t is not passed:
        #     We decide to pass it here.
        #     We add a[t] to our preparation requirement.
        #     Mark t as passed.
        #   If exam t is already passed:
        #     This day can be used for preparation for other exams.
        # When we encounter a day with 0:
        #   This day can be used for preparation.
        
        # After iterating all days, if the total preparation days required <= total free days available, it's valid.
        # But wait, the "free days" are the days we didn't use for passing exams.
        # Let's refine:
        # Total days = k.
        # Number of exams passed = m.
        # Total preparation days needed = sum(a).
        # Total days occupied by exams = m.
        # Total days needed = m + sum(a).
        # But we can only use days <= k.
        # Also, the preparation days must be strictly before the exam day.
        
        # Greedy check:
        # 1. Identify the latest day <= k for each exam type. If any exam type has no day <= k, return False.
        # 2. Sort these latest days.
        # 3. Iterate backwards from k to 1.
        #    Maintain a variable `prep_days_needed` which accumulates the preparation days for exams we decided to pass.
        #    Actually, simpler:
        #    We iterate backwards. We keep a set of exams we need to pass.
        #    If current day has exam type t:
        #      If t is in needed_exams:
        #        We pass it here. Remove t from needed_exams.
        #        Add a[t] to `days_needed_for_prep`.
        #      Else:
        #        This day is free for prep.
        #    If current day is 0:
        #      This day is free for prep.
        #    
        #    After the loop, we have `days_needed_for_prep` total preparation days required.
        #    The number of days available for preparation is `k - m` (since we pass m exams).
        #    But we must ensure that for each exam, the preparation days can fit before its exam day.
        #    Since we process backwards, when we are at day `d` (exam day), we have accumulated all preparation needs for exams passed at `d` and later.
        #    Wait, the preparation for an exam passed at day `d` must happen on days < `d`.
        #    So, as we iterate backwards:
        #      Let `current_free_days` be the count of free days encountered so far (from k down to current).
        #      When we encounter an exam day for an exam we haven't passed yet:
        #        We commit to passing it here.
        #        We add its preparation time to `total_prep_needed`.
        #        We check if `current_free_days` >= `total_prep_needed`? 
        #        No, because `total_prep_needed` includes prep for exams passed at LATER days (which we already processed).
        #        The prep for the current exam must be done BEFORE this day.
        #        So, at the moment we decide to pass exam `t` at day `d`, we need to have enough free days in the range [1, d-1].
        #        But we don't know the future (forward) yet.
        #        
        #    Alternative view:
        #    Total preparation days = S = sum(a).
        #    Total exam days = m.
        #    Total days required = S + m.
        #    If S + m > k, impossible.
        #    But position matters.
        #    
        #    Correct Greedy Strategy (Backward):
        #    1. For each exam i, find the latest day <= k where d[day] == i. If none, return False.
        #    2. Store these days in a list `exam_days`.
        #    3. Sort `exam_days` in ascending order.
        #    4. Iterate through `exam_days` from left to right (earliest exam day to latest).
        #       Let the current exam day be `d`.
        #       We need to reserve `a[i]` days for preparation BEFORE `d`.
        #       The available days before `d` are `d - 1`.
        #       However, some of these days might be used by other exams passed earlier.
        #       Let `used_days` be the number of days occupied by exams passed so far (including current).
        #       Actually, let's track `days_consumed` which is the number of days used for exams and their prep.
        #       This is tricky because prep days are flexible.
        #       
        #    Let's try the standard solution pattern for this problem:
        #    Iterate backwards from k to 1.
        #    Keep a set of exams that are NOT yet passed.
        #    Keep a counter `prep_needed` = 0.
        #    Keep a counter `free_days` = 0.
        #    For day i from k down to 1:
        #      If d[i-1] == 0:
        #        free_days += 1
        #      Else:
        #        exam_type = d[i-1]
        #        If exam_type is not in passed_set:
        #          # We must pass this exam on this day (latest opportunity)
        #          passed_set.add(exam_type)
        #          prep_needed += a[exam_type - 1]
        #        Else:
        #          # Exam already passed, this day is free for prep
        #          free_days += 1
        #    
        #    After the loop, we have `prep_needed` total preparation days required.
        #    We have `free_days` total free days available in the schedule (days not used for passing exams).
        #    Is `free_days >= prep_needed`?
        #    Wait, this logic assumes that any free day can be used for any prep.
        #    But prep for an exam passed at day `d` must be on days < `d`.
        #    In the backward pass, when we are at day `d` (exam day), we add `a[exam]` to `prep_needed`.
        #    The `free_days` accumulated so far are from days `k` down to `d+1`. These are AFTER `d`. They cannot be used for prep for exam at `d`.
        #    So this simple check `free_days >= prep_needed` is WRONG because it mixes future free days with current prep needs.
        
        #    Correct Logic with Backward Pass:
        #    We need to ensure that for every exam passed at day `d`, the sum of preparation days for all exams passed at days `>= d` can fit in the days `< d`.
        #    Let's accumulate `prep_needed` as we go backwards.
        #    Let `free_days_before` be the number of free days encountered so far (which are < current day).
        #    Wait, iterating backwards:
        #    When at day `i`:
        #      If it's an exam day for an unpassed exam:
        #        We pass it.
        #        We add `a[exam]` to `total_prep_needed`.
        #        Now, we need to check if we have enough free days in the range [1, i-1] to cover `total_prep_needed`.
        #        But we haven't processed [1, i-1] yet in the backward loop.
        #        
        #    Let's switch to Forward simulation with the constraints derived from Backward? No.
        #    Let's re-evaluate the condition.
        #    We have a set of exam days: $d_1 < d_2 < ... < d_m$.
        #    For each $j$, we need to fit $a_{exam_j}$ preparation days in $[1, d_j - 1]$.
        #    Also, the intervals $[1, d_1-1], [d_1+1, d_2-1], ...$ are available.
        #    Actually, the exams consume the days $d_1, d_2, ...$.
        #    The preparation days can be anywhere before the respective exam day.
        #    So, for the first exam at $d_1$, we need $a_1$ days in $[1, d_1-1]$.
        #    For the second exam at $d_2$, we need $a_2$ days in $[1, d_2-1] \setminus \{d_1\}$.
        #    Generally, for the $j$-th exam (sorted by day), we need $a_{exam_j}$ days in $[1, d_j-1]$ excluding the $j-1$ exam days used by previous exams.
        #    So, the condition is:
        #      For all $j=1..m$:
        #        $(d_j - 1) - (j - 1) \ge \sum_{k=1}^j a_{exam_k}$
        #    Wait, is this correct?
        #    The LHS is the number of available days before $d_j$ minus the days taken by previous exams.
        #    The RHS is the total preparation needed for exams $1..j$.
        #    Since prep for exam $k$ ($k \le j$) must be before $d_k$ (which is $\le d_j$), all these prep days must be in $[1, d_j-1]$.
        #    And they must not overlap with exam days $d_1, ..., d_{j-1}$.
        #    So yes, the total capacity before $d_j$ is $(d_j - 1) - (j - 1)$.
        #    The total demand is $\sum_{k=1}^j a_{exam_k}$.
        #    So we need $(d_j - j) \ge \sum_{k=1}^j a_{exam_k}$ for all $j$.
        #    Also, we need $d_m \le k$.
        #    And obviously $d_j$ must exist for all exams.
        
        #    Algorithm:
        #    1. For each exam type $1..m$, find the latest day $\le k$ where it appears.
        #       If any exam type is missing, return False.
        #    2. Collect these days into a list `days`.
        #    3. Sort `days`.
        #    4. Iterate $j$ from 0 to $m-1$:
        #       current_day = days[j]
        #       exam_idx = exam_type corresponding to days[j]
        #       needed = a[exam_idx - 1]
        #       total_needed += needed
        #       available = current_day - 1 - j  # days before current_day minus j previous exam days
        #       if available < total_needed:
        #         return False
        #    5. return True

        # Implementation details:
        # We need to map exam type to its latest day.
        # Since we iterate 1 to k, we can just record the last occurrence.
        
        last_occurrence = {}
        for day in range(1, k + 1):
            val = d[day - 1]
            if val != 0:
                last_occurrence[val] = day
        
        # Check if all exams 1..m are present
        for i in range(1, m + 1):
            if i not in last_occurrence:
                return False
        
        days = sorted([last_occurrence[i] for i in range(1, m + 1)])
        
        total_prep = 0
        for j in range(m):
            exam_type = days[j] # This is the day number, but we need the exam type
            # Wait, `days` contains the day numbers. We need to know which exam type is on that day.
            # We can reconstruct the exam type from `last_occurrence` values?
            # No, `last_occurrence` maps exam_type -> day.
            # We need the inverse or just store pairs.
            pass
        
        # Let's store pairs (day, exam_type)
        exam_schedule = []
        for exam_type in range(1, m + 1):
            day = last_occurrence[exam_type]
            exam_schedule.append((day, exam_type))
        
        exam_schedule.sort(key=lambda x: x[0])
        
        total_prep = 0
        for j in range(m):
            day, exam_type = exam_schedule[j]
            prep_needed = a[exam_type - 1]
            total_prep += prep_needed
            # Available days before `day` excluding `j` exam days
            available = day - 1 - j
            if available < total_prep:
                return False
                
        return True

    # Binary search
    low = 1
    high = n
    ans = -1
    
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
            
    print(ans)

if __name__ == '__main__':
    solve()