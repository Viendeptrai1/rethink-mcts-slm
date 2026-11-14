import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    D = int(data[0])
    G = int(data[1])
    
    p = []
    c = []
    idx = 2
    for _ in range(D):
        p.append(int(data[idx]))
        c.append(int(data[idx+1]))
        idx += 2
    
    # Precompute total base score and problem count for each type i
    # type i has score 100*(i+1)
    # We will iterate over all subsets of types that are fully solved.
    
    min_problems = float('inf')
    
    # There are 2^D subsets. D <= 10, so 1024 iterations max.
    for mask in range(1 << D):
        current_score = 0
        current_problems = 0
        possible = True
        
        # Calculate score and problem count for fully solved types in this mask
        for i in range(D):
            if (mask >> i) & 1:
                # Type i is fully solved
                score_per_problem = 100 * (i + 1)
                bonus = c[i]
                count = p[i]
                
                base_score = count * score_per_problem
                total_score = base_score + bonus
                
                current_score += total_score
                current_problems += count
        
        if current_score >= G:
            min_problems = min(min_problems, current_problems)
            continue
        
        remaining_needed = G - current_score
        
        if remaining_needed <= 0:
            min_problems = min(min_problems, current_problems)
            continue
        
        # Now we need to fill the remaining_needed score using a subset of the remaining types.
        # To minimize the number of problems, we should greedily pick from the remaining types
        # that have the smallest score per problem (i.e., smallest index) because they give the most problems per point?
        # Wait, no. We want to minimize the COUNT of problems.
        # Score per problem for type i is 100*(i+1).
        # If we take one problem of type i, we get 100*(i+1) points and count 1.
        # To minimize count, we want to maximize points per problem. So we should pick types with HIGHER scores first?
        # Let's re-evaluate.
        # We need to reach 'remaining_needed' points.
        # Each problem of type i gives S_i = 100*(i+1) points and costs 1 problem.
        # We want to minimize sum(count_i) such that sum(count_i * S_i) >= remaining_needed.
        # This is equivalent to: minimize sum(count_i) subject to sum(count_i * S_i) >= R.
        # Since S_i increases with i, a problem of type D gives the most points per problem.
        # So intuitively, we should take problems from the highest score types first to minimize count?
        # HOWEVER, there is a constraint: we can only take a problem of type i if we haven't fully solved it yet?
        # No, the problem statement says: "when a user solves all problems with a score of 100i points, he/she earns the perfect bonus".
        # It does NOT say we cannot solve partial sets. We can solve any number of problems of type i (from 1 to p_i).
        # If we solve all p_i problems of type i, we get the bonus c_i.
        # In our current approach, we are iterating over subsets of types that are FULLY solved.
        # The remaining types are NOT fully solved.
        # For the remaining types, we can choose to solve some number of problems (0 to p_i - 1) to fill the gap.
        # BUT, if we solve p_i problems of a remaining type, we effectively trigger the bonus.
        # However, our outer loop iterates over ALL subsets of fully solved types.
        # So if we decide to fully solve type j in the "filling" phase, that case would have been covered when the mask included j.
        # Therefore, in the filling phase, for any type i NOT in the mask, we can solve at most p_i - 1 problems.
        # Actually, strictly speaking, if we solve p_i problems, we get the bonus.
        # If we solve p_i problems, the total score contribution is p_i * S_i + c_i.
        # This is exactly the same as if type i was in the "fully solved" set.
        # So, to avoid double counting or missing cases, we can enforce that for types not in the mask,
        # we solve strictly less than p_i problems.
        # But wait, what if the optimal solution involves fully solving type j, but we didn't include it in the mask?
        # Then our calculation for the mask without j would try to fill the gap using < p_j problems of type j.
        # This would yield a lower score than the full solution, so it wouldn't be optimal for that specific gap.
        # But maybe the mask without j + partial j is better than mask with j?
        # No, because mask with j gives more score for the same number of problems (p_j) plus bonus.
        # So if the optimal solution fully solves j, the mask including j will find it.
        # The only risk is if the optimal solution fully solves j, but we are in a mask that doesn't include j,
        # and we try to fill the gap. We would stop at p_j - 1. The score would be insufficient.
        # So we just need to ensure that for types not in the mask, we take at most p_i - 1 problems.
        # And for types in the mask, we have already taken p_i problems.
        
        # Strategy for filling:
        # We have a list of available types (those not in mask).
        # For each such type i, we can take k_i problems where 0 <= k_i <= p_i - 1.
        # We want to minimize sum(k_i) such that sum(k_i * S_i) >= remaining_needed.
        # Since we want to minimize the count, and each problem gives S_i points,
        # we should prioritize types with the LARGEST S_i?
        # Let's check: Suppose we need 100 points.
        # Type 0: 100 pts/problem. Type 1: 200 pts/problem.
        # If we take 1 of Type 1, count=1. If we take 1 of Type 0, count=1.
        # Suppose we need 150 points.
        # Type 0: need 2 problems (200 pts). Count=2.
        # Type 1: need 1 problem (200 pts). Count=1.
        # Clearly, taking higher score problems reduces the count.
        # So we should greedily take problems from the remaining types in DECREASING order of score (i.e., from D-1 down to 0).
        # BUT, there is a catch.
        # What if taking a high score problem forces us to take more problems of a lower score type later?
        # No, because we are just summing up points. The "cost" is always 1 per problem regardless of type.
        # To minimize count, we want each problem to contribute as much as possible.
        # So yes, we should always pick the available problem type with the highest score per problem first.
        # However, we must respect the limit p_i - 1 for types not in the mask.
        
        # Wait, is it possible that taking a lower score problem is better?
        # No. Because if we replace a high score problem with a low score problem, we get fewer points for the same count.
        # To reach the target, we would need MORE problems.
        # So the greedy strategy of taking highest score problems first is correct for minimizing count.
        
        # Let's refine the filling strategy:
        # Iterate i from D-1 down to 0.
        # If type i is in the mask, skip (already fully solved).
        # If type i is not in the mask:
        #   We can take at most p[i] - 1 problems.
        #   How many do we need?
        #   needed = remaining_needed
        #   max_take = p[i] - 1
        #   if needed <= 0: break
        #   take = min(needed // S_i, max_take)
        #   current_problems += take
        #   current_score += take * S_i
        #   remaining_needed -= take * S_i
        #   if remaining_needed <= 0: break
        
        # Is this correct?
        # Consider the case where we need 100 points.
        # Available: Type 0 (100 pts, p=1), Type 1 (200 pts, p=1).
        # Mask is empty.
        # We iterate from D-1 (Type 1).
        # max_take = 0 (since p=1, we can take at most 0).
        # So we take 0.
        # Then Type 0. max_take = 0. Take 0.
        # Result: 0 points. Fails.
        # But the optimal solution is to fully solve Type 0 (1 problem, 100+bonus).
        # This case is covered when the mask includes Type 0.
        # So in the mask=empty case, we correctly determine we can't reach the goal without fully solving some types.
        # The algorithm will try other masks.
        
        # One edge case: What if the optimal solution involves fully solving type j, but we are in a mask that doesn't include j,
        # and we try to fill the gap?
        # As reasoned, we will take at most p_j - 1 problems of type j.
        # The score will be less than the full solution.
        # So the condition `current_score >= G` will fail.
        # We will move to the next mask.
        # Eventually, the mask that includes j will be tried, and it will find the solution.
        # So this logic holds.
        
        # Wait, there is a subtle issue.
        # What if the optimal solution is: Fully solve Type A, and partially solve Type B.
        # Our mask includes A. We fill with B. Correct.
        # What if the optimal solution is: Partially solve Type A, Fully solve Type B.
        # Our mask includes B. We fill with A. Correct.
        # What if the optimal solution is: Fully solve Type A and Type B.
        # Our mask includes both. Correct.
        # What if the optimal solution is: Partially solve Type A and Type B.
        # Our mask includes neither. We fill with A and B. Correct.
        
        # So the logic seems sound.
        
        # Let's re-verify the greedy filling order.
        # We want to minimize count.
        # We have a set of items (problem types) with values S_i and capacities cap_i = p_i - 1.
        # We want to select items to get sum >= R with min count.
        # Since each item has weight 1 (count), and value S_i,
        # we should pick items with largest S_i first.
        # Yes, this is correct.
        
        # Implementation details:
        # S_i = 100 * (i + 1)
        
        temp_score = current_score
        temp_problems = current_problems
        temp_needed = remaining_needed
        
        # Iterate from highest score type to lowest
        for i in range(D - 1, -1, -1):
            if (mask >> i) & 1:
                continue
            
            score_per_problem = 100 * (i + 1)
            max_take = p[i] - 1
            
            if temp_needed <= 0:
                break
            
            if max_take <= 0:
                continue
            
            # How many can we take?
            # We need to cover temp_needed.
            # Each problem gives score_per_problem.
            # Number of problems needed to cover temp_needed is ceil(temp_needed / score_per_problem).
            # But we are limited by max_take.
            # Also, we might not need to take the full amount if we overshoot.
            # We just take as many as possible up to max_take, or enough to cover.
            
            # Actually, we should take min(max_take, ceil(temp_needed / score_per_problem))?
            # No, we should take enough to cover, but capped by max_take.
            # If max_take is enough to cover, we take ceil(temp_needed / score_per_problem).
            # If max_take is not enough, we take max_take.
            
            # Let's calculate how many are needed to cover the rest.
            # needed_count = (temp_needed + score_per_problem - 1) // score_per_problem
            # take = min(max_take, needed_count)
            # But wait, if we take 'take' problems, the score added is take * score_per_problem.
            # If take < needed_count, then we still have a gap.
            # But we are iterating through all types. The next type (lower score) will fill the rest.
            # So we should take as many as possible from the current type to minimize the count?
            # Yes, because current type has higher score than any subsequent type.
            # So taking more from current type is always better than taking from lower types.
            # So we take min(max_take, ceil(temp_needed / score_per_problem))?
            # Actually, if we take max_take and it's not enough, we just take max_take and move to next.
            # If we take enough to cover, we stop.
            # So:
            # take = min(max_take, (temp_needed + score_per_problem - 1) // score_per_problem)
            # But wait, if (temp_needed + score_per_problem - 1) // score_per_problem is 0?
            # That means temp_needed is 0, which is handled.
            
            # Let's simplify:
            # We want to reduce temp_needed.
            # We can take up to max_take.
            # Each unit reduces temp_needed by score_per_problem.
            # We should take as many as possible, up to the point where temp_needed becomes <= 0.
            # So:
            # take = min(max_take, (temp_needed + score_per_problem - 1) // score_per_problem)
            # But if temp_needed is very large, we take max_take.
            # If temp_needed is small, we take ceil.
            
            # Wait, is it possible that taking max_take is worse than taking less?
            # No, because we want to minimize total count.
            # Taking more from a high-value item is always better than taking from a low-value item.
            # So we take as many as possible, up to the amount needed to finish.
            
            # Correct logic:
            # take = min(max_take, (temp_needed + score_per_problem - 1) // score_per_problem)
            # But wait, if temp_needed is 100, score=200. ceil(100/200) = 1.
            # We take 1. Score added 200. temp_needed becomes -100. Done.
            # If temp_needed is 300, score=200. ceil(300/200) = 2.
            # We take 2. Score added 400. temp_needed becomes -100. Done.
            # If max_take is 1.
            # take = min(1, 2) = 1.
            # Score added 200. temp_needed becomes 100.
            # Next type (lower score) will handle the rest.
            
            # This seems correct.
            
            needed_count = (temp_needed + score_per_problem - 1) // score_per_problem
            take = min(max_take, needed_count)
            
            if take > 0:
                temp_problems += take
                temp_score += take * score_per_problem
                temp_needed -= take * score_per_problem
                
                if temp_needed <= 0:
                    break
        
        if temp_needed <= 0:
            min_problems = min(min_problems, temp_problems)

    print(min_problems)

if __name__ == '__main__':
    solve()