import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    D = int(next(iterator))
    G = int(next(iterator))
    
    problems = []
    for _ in range(D):
        p = int(next(iterator))
        c = int(next(iterator))
        problems.append({'p': p, 'c': c, 'score': 100 * (_ + 1)})
    
    min_problems = D * 100 + 1
    
    # Try all possible subsets of problems to get perfect bonuses
    # Since D <= 10, we can iterate through 2^D possibilities
    for mask in range(1 << D):
        current_base_score = 0
        current_problems = 0
        possible = True
        
        for i in range(D):
            if (mask >> i) & 1:
                # Choose to get perfect bonus for category i
                p_i = problems[i]['p']
                current_base_score += p_i * problems[i]['score']
                current_problems += p_i
            else:
                # Do not get perfect bonus for category i
                possible = False
                break
        
        if not possible:
            continue
        
        # Calculate total score including bonuses
        total_score = current_base_score
        for i in range(D):
            if (mask >> i) & 1:
                total_score += problems[i]['c']
        
        if total_score >= G:
            min_problems = min(min_problems, current_problems)
    
    # If no subset with perfect bonuses works, try adding problems one by one to the best subset found so far
    # Actually, the above loop only considers full categories for perfect bonuses.
    # We need to consider cases where we don't get a perfect bonus for a category but solve some problems in it.
    
    # Let's restart with a different approach:
    # Iterate over all subsets of categories for which we get perfect bonuses.
    # For the remaining categories, we might solve some problems (but not all, unless they are needed to reach G).
    
    # Actually, the optimal strategy for a fixed set of perfect bonuses is:
    # 1. Solve all problems in categories chosen for perfect bonuses.
    # 2. For categories not chosen for perfect bonuses, solve problems one by one starting from the highest score category
    #    until the total score reaches G.
    
    min_problems = D * 100 + 1
    
    for mask in range(1 << D):
        current_base_score = 0
        current_problems = 0
        
        for i in range(D):
            if (mask >> i) & 1:
                # Get perfect bonus for category i
                p_i = problems[i]['p']
                score_i = problems[i]['score']
                c_i = problems[i]['c']
                current_base_score += p_i * score_i
                current_problems += p_i
                current_base_score += c_i
            else:
                # Don't get perfect bonus for category i
                # We might still solve some problems in this category
                pass
        
        if current_base_score >= G:
            min_problems = min(min_problems, current_problems)
        else:
            # Need to solve more problems from categories not in mask
            # Sort remaining categories by score descending
            remaining_categories = []
            for i in range(D):
                if not ((mask >> i) & 1):
                    remaining_categories.append((problems[i]['score'], problems[i]['p']))
            
            # Sort by score descending
            remaining_categories.sort(key=lambda x: x[0], reverse=True)
            
            for score, p in remaining_categories:
                needed = G - current_base_score
                # Each problem gives 'score' points
                num_to_solve = (needed + score - 1) // score
                if num_to_solve <= p:
                    current_problems += num_to_solve
                    current_base_score += num_to_solve * score
                    break
                else:
                    current_problems += p
                    current_base_score += p * score
            
            if current_base_score >= G:
                min_problems = min(min_problems, current_problems)
    
    print(min_problems)

if __name__ == '__main__':
    solve()