import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    exams = []
    for i in range(m):
        s = int(next(iterator))
        d = int(next(iterator))
        c = int(next(iterator))
        exams.append({'id': i + 1, 's': s, 'd': d, 'c': c, 'rem': c})

    schedule = [0] * (n + 1)  # 1-based indexing for days

    # Sort exams by deadline (d_i)
    exams_sorted = sorted(exams, key=lambda x: x['d'])

    # We will try to schedule exams in order of their deadlines.
    # For each exam, we need to find 'rem' days in the range [s, d-1] that are currently free.
    # Since we process exams by increasing deadline, we are filling slots for urgent exams first.
    # However, simply picking any free day might not be optimal if a later exam (with a later deadline)
    # has a window that is a subset of the current exam's window. But wait, if we process by deadline,
    # the current exam has the earliest deadline among remaining. Its window ends at d-1.
    # Any other exam we haven't processed yet has a deadline >= current d.
    # So their windows end at >= current d.
    # The critical constraint is that we must pick days <= d-1.
    # If we pick days as late as possible (closest to d-1), we might block an exam that has a deadline
    # exactly at d (which is the current one) or later? No, the current one is the most urgent.
    # Actually, the standard greedy strategy for this problem is:
    # Iterate days from 1 to n. On day j, if it's an exam day, mark it.
    # If it's a preparation day, assign it to the exam with the earliest deadline that is valid (s_i <= j < d_i) and still needs preparation.
    # Why earliest deadline? Because if we don't prepare for the most urgent exam now, we might miss its deadline.
    # Exams with later deadlines can wait.
    
    # Let's re-verify the "Earliest Deadline First" on chronological days.
    # Day 1 to n:
    #   If day j is an exam day for exam k: schedule[j] = k+1 (or m+1 as per problem statement? 
    #   Problem says: print (m+1) if it's an exam day. Wait, "recall that in each day no more than one exam is conducted".
    #   And output format: "(m + 1), if the j-th day is a day of some exam".
    #   So if day j is the exam day for exam i, we output m+1.
    #   If day j is preparation for exam i, we output i.
    #   Else 0.
    
    # Algorithm:
    # 1. Identify which exam is on which day. Since exams are on distinct days, we can map day -> exam_id.
    # 2. Iterate day j from 1 to n.
    # 3. If day j is an exam day for exam E:
    #      Check if E has been fully prepared. If not, impossible -> print -1.
    #      Mark day j as exam day (value m+1).
    # 4. If day j is not an exam day:
    #      Find all exams that are:
    #        a) Not yet finished (rem > 0)
    #        b) Valid to prepare on day j (s_i <= j < d_i)
    #      Among these, pick the one with the smallest d_i (earliest deadline).
    #      If multiple have same d_i, any is fine (or smallest id).
    #      If no such exam exists, day j is rest (0).
    #      If we pick exam E, decrement rem, set schedule[j] = E.id.
    
    # Let's trace Example 2:
    # 3 days, 2 exams.
    # Exam 1: 1 3 1 (s=1, d=3, c=1). Window [1, 2].
    # Exam 2: 1 2 1 (s=1, d=2, c=1). Window [1, 1].
    # Day 1: Not exam day. Candidates: Exam 1 (d=3), Exam 2 (d=2). Earliest deadline is Exam 2.
    #   Assign Exam 2. rem[2]=0. Schedule[1]=2.
    # Day 2: Exam day for Exam 1? Yes (d=3? No, d=3 is day 3). Wait.
    #   Exam 1: d=3. Exam 2: d=2.
    #   Day 2 is exam day for Exam 2.
    #   Check if Exam 2 is prepared. rem[2] is 0. OK.
    #   Schedule[2] = m+1 = 3.
    # Day 3: Exam day for Exam 1.
    #   Check if Exam 1 is prepared. rem[1] is 1 (not done).
    #   Impossible. Output -1. Correct.
    
    # Trace Example 1:
    # 5 2
    # 1: 1 3 1 (d=3)
    # 2: 1 5 1 (d=5)
    # Day 1: Candidates: 1 (d=3), 2 (d=5). Pick 1. S[1]=1. rem[1]=0.
    # Day 2: Not exam. Candidates: 2 (d=5). Pick 2. S[2]=2. rem[2]=0.
    # Day 3: Exam 1. Prepared? Yes. S[3]=3 (m+1=3).
    # Day 4: Not exam. Candidates: None (both done). S[4]=0.
    # Day 5: Exam 2. Prepared? Yes. S[5]=3.
    # Result: 1 2 3 0 3. Matches example.
    
    # Trace Example 3:
    # 10 3
    # 1: 4 7 2 (d=7)
    # 2: 1 10 3 (d=10)
    # 3: 8 9 1 (d=9)
    # Day 1: Cand: 1 (d=7), 2 (d=10). Pick 1. S[1]=1. rem[1]=1.
    # Day 2: Cand: 1 (d=7), 2 (d=10). Pick 1. S[2]=1. rem[1]=0.
    # Day 3: Cand: 2 (d=10). Pick 2. S[3]=2. rem[2]=2.
    # Day 4: Exam 1? No, d=7. Exam 1 s=4. So day 4 is valid for prep.
    #   Wait, is day 4 an exam day? No.
    #   Cand: 2 (d=10). Pick 2. S[4]=2. rem[2]=1.
    # Day 5: Cand: 2. Pick 2. S[5]=2. rem[2]=0.
    # Day 6: Cand: 2? No, rem=0. Cand: 3? s=8, d=9. Day 6 < 8. Not valid.
    #   So rest. S[6]=0.
    # Day 7: Exam 1 (d=7). Prepared? Yes. S[7]=4.
    # Day 8: Exam 3? No, d=9. s=8. Valid for prep.
    #   Cand: 3 (d=9). Pick 3. S[8]=3. rem[3]=0.
    # Day 9: Exam 3 (d=9). Prepared? Yes. S[9]=4.
    # Day 10: Exam 2 (d=10). Prepared? Yes. S[10]=4.
    # Result: 1 1 2 2 2 0 4 3 4 4.
    # Example output: 2 2 2 1 1 0 4 3 4 4.
    # My result is different but valid?
    # My result:
    # Day 1: Exam 1 prep.
    # Day 2: Exam 1 prep.
    # Day 3: Exam 2 prep.
    # Day 4: Exam 2 prep.
    # Day 5: Exam 2 prep.
    # Day 6: Rest.
    # Day 7: Exam 1.
    # Day 8: Exam 3 prep.
    # Day 9: Exam 3.
    # Day 10: Exam 2.
    # Checks:
    # Exam 1: s=4, d=7, c=2. Prep days 1, 2. Both in [4, 6]? NO!
    # s_i <= j < d_i. For Exam 1, s=4, d=7. Valid days: 4, 5, 6.
    # My schedule put prep on 1, 2. Invalid!
    
    # Ah, the condition is s_i <= j < d_i.
    # In my trace for Day 1: Exam 1 has s=4. So Exam 1 is NOT valid on Day 1.
    # So on Day 1, only Exam 2 is valid (s=1).
    # Let's re-trace carefully.
    
    # Exams:
    # 1: s=4, d=7, c=2
    # 2: s=1, d=10, c=3
    # 3: s=8, d=9, c=1
    
    # Day 1:
    #   Exam 1: s=4 > 1. Invalid.
    #   Exam 2: s=1 <= 1 < 10. Valid.
    #   Exam 3: s=8 > 1. Invalid.
    #   Pick Exam 2. S[1]=2. rem[2]=2.
    # Day 2:
    #   Exam 1: s=4 > 2. Invalid.
    #   Exam 2: Valid.
    #   Exam 3: Invalid.
    #   Pick Exam 2. S[2]=2. rem[2]=1.
    # Day 3:
    #   Exam 1: s=4 > 3. Invalid.
    #   Exam 2: Valid.
    #   Exam 3: Invalid.
    #   Pick Exam 2. S[3]=2. rem[2]=0.
    # Day 4:
    #   Exam 1: s=4 <= 4 < 7. Valid.
    #   Exam 2: s=1 <= 4 < 10. Valid.
    #   Exam 3: Invalid.
    #   Deadlines: Exam 1 (7), Exam 2 (10). Earliest is Exam 1.
    #   Pick Exam 1. S[4]=1. rem[1]=1.
    # Day 5:
    #   Exam 1: Valid.
    #   Exam 2: Valid.
    #   Pick Exam 1. S[5]=1. rem[1]=0.
    # Day 6:
    #   Exam 1: Valid (4<=6<7). But rem=0.
    #   Exam 2: Valid.
    #   Pick Exam 2. S[6]=2. rem[2]=-1? No, rem was 0.
    #   Wait, rem[2] became 0 on Day 3.
    #   So on Day 6, Exam 2 is not a candidate (rem=0).
    #   Exam 1 is not a candidate (rem=0).
    #   Rest. S[6]=0.
    # Day 7:
    #   Exam 1: d=7. Exam day. Check rem[1]=0. OK. S[7]=4.
    # Day 8:
    #   Exam 1: d=7. Not valid (j < d).
    #   Exam 2: Valid. But rem=0.
    #   Exam 3: s=8 <= 8 < 9. Valid.
    #   Pick Exam 3. S[8]=3. rem[3]=0.
    # Day 9:
    #   Exam 3: d=9. Exam day. Check rem[3]=0. OK. S[9]=4.
    # Day 10:
    #   Exam 2: d=10. Exam day. Check rem[2]=0. OK. S[10]=4.
    # Result: 2 2 2 1 1 0 4 3 4 4.
    # Matches example output exactly.
    
    # So the logic holds:
    # 1. Map exam_id to (s, d, c, rem).
    # 2. Map day -> exam_id (for exam days).
    # 3. Iterate j from 1 to n.
    # 4. If j is exam day for exam E:
    #      If rem[E] > 0: return -1.
    #      schedule[j] = m + 1.
    # 5. Else:
    #      Find candidates: exams where rem > 0 AND s <= j < d.
    #      If no candidates: schedule[j] = 0.
    #      Else: pick candidate with min d. If tie, min id.
    #      Decrement rem, set schedule[j] = id.
    
    # Implementation details:
    # - Store exams in a list.
    # - Create an array `exam_on_day` of size n+1, init to 0.
    # - Fill `exam_on_day` from input.
    # - Loop j 1..n.
    
    exam_on_day = [0] * (n + 1)
    for i in range(m):
        d = exams[i]['d']
        exam_on_day[d] = exams[i]['id']
    
    # We need to access exams by ID quickly.
    # Let's create a list of exam objects and maybe a dict or just iterate the list (m is small, <= 100).
    # Iterating m=100 items for each of n=100 days is 10000 ops, perfectly fine.
    
    for j in range(1, n + 1):
        eid = exam_on_day[j]
        if eid != 0:
            # It's an exam day
            # Check if prepared
            if exams[eid-1]['rem'] > 0:
                print("-1")
                return
            schedule[j] = m + 1
        else:
            # Preparation day or rest
            candidates = []
            for i in range(m):
                e = exams[i]
                if e['rem'] > 0 and e['s'] <= j < e['d']:
                    candidates.append((e['d'], e['id']))
            
            if not candidates:
                schedule[j] = 0
            else:
                # Sort by deadline, then by id
                candidates.sort(key=lambda x: (x[0], x[1]))
                best = candidates[0]
                schedule[j] = best[1]
                exams[best[1]-1]['rem'] -= 1

    # Output
    print(*(schedule[1:]))

if __name__ == '__main__':
    solve()