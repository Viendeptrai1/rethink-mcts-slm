import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        k = int(next(iterator))
    except StopIteration:
        return

    a = []
    b = []
    c = []
    
    for _ in range(n):
        a.append(int(next(iterator)))
        b.append(int(next(iterator)))
        c.append(int(next(iterator)))

    portals = []
    for _ in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        # Convert to 0-based index
        portals.append((u - 1, v - 1))

    # Precompute portals for each castle
    # adj[i] contains list of v such that there is a portal from i to v
    adj = [[] for _ in range(n)]
    for u, v in portals:
        adj[u].append(v)

    # DP state: dp[i][w] = max score achievable after capturing castle i (0-indexed)
    # with exactly w warriors remaining in the army.
    # However, w can be up to 5000. N is up to 5000.
    # We need to be careful with memory and time.
    # Since we process castles in order 0 to n-1, we can maintain a DP array for the current step.
    # dp[w] = max score with w warriors after processing some prefix of castles.
    
    # Max possible warriors is 5000 as per problem statement.
    MAX_WARRIORS = 5000
    
    # Initialize DP: before capturing any castle, we have k warriors and score 0.
    # We use a dictionary or a list. A list is faster if dense, but many states might be unreachable.
    # Given constraints and nature of the problem, a list of size 5001 is feasible.
    # Initialize with -1 to represent unreachable states.
    dp = [-1] * (MAX_WARRIORS + 1)
    dp[k] = 0
    
    # We also need to track the maximum reachable warrior count to optimize loops
    max_reachable = k
    
    for i in range(n):
        req = a[i]
        hire = b[i]
        val = c[i]
        
        # Check if it's possible to capture this castle with current max warriors
        if max_reachable < req:
            print("-1")
            return
        
        new_dp = [-1] * (MAX_WARRIORS + 1)
        new_max_reachable = 0
        
        # Iterate over all possible current army sizes w
        # We only care about w >= req
        # Optimization: iterate from min(max_reachable, MAX_WARRIORS) down to req
        # But we need to consider all reachable states.
        
        # Let's find the range of reachable w
        start_w = req
        end_w = min(max_reachable, MAX_WARRIORS)
        
        # We will collect valid (w, score) pairs to process
        # To avoid iterating over -1s, we can keep a list of reachable w, 
        # but given N=5000 and W=5000, O(N*W) is 2.5e7 which is acceptable in Python if operations are simple.
        # Let's try direct iteration with pruning.
        
        for w in range(start_w, end_w + 1):
            if dp[w] == -1:
                continue
            
            current_score = dp[w]
            
            # Option 1: Do nothing special regarding defense yet (just capture and hire)
            # After capturing, we have w warriors. We need at least 'req' to capture.
            # We hire 'hire' warriors.
            # New army size before defense actions: w + hire
            # But wait, the problem says:
            # "After you capture the castle i ... you may recruit new warriors ... leave a warrior ... use portals"
            # The recruitment happens immediately after capture.
            # So available warriors for defense = w + hire.
            # However, we must ensure we have enough to capture first.
            # We checked w >= req.
            
            available = w + hire
            
            # We can defend some castles. Each defense costs 1 warrior.
            # We can defend castle i directly (cost 1, gain val).
            # We can defend castle v via portal from i (cost 1, gain c[v]).
            # Note: We can only use portals from i. We cannot chain portals.
            # Also, we can defend castle i itself.
            
            # The set of castles we can defend from castle i is:
            # {i} U {v | (i, v) in portals}
            
            # We want to choose a subset of these to defend such that:
            # (available - number_defended) >= 0 (actually, we just need to survive, 
            # but the constraint is usually about having enough for the NEXT castle).
            # Wait, the constraint is: "If, during some moment in the game, you don't have enough warriors to capture the next castle, you lose."
            # The "next castle" is i+1.
            # So after all actions at castle i, the remaining army size must be >= a[i+1] (if i+1 exists).
            # If i is the last castle, there is no next castle, so remaining army size can be anything >= 0.
            
            # Let's formalize:
            # Let S be the set of castles defended from i.
            # Cost = len(S).
            # Remaining warriors = available - len(S).
            # Constraint: If i < n-1, remaining warriors >= a[i+1].
            # Objective: Maximize current_score + sum(c[x] for x in S).
            
            # Since we want to maximize score, and each defense costs 1 warrior,
            # this looks like a knapsack-like problem but simpler because all items (castles to defend) have weight 1.
            # We should greedily pick the ones with highest importance?
            # Yes, because the cost is uniform (1 warrior per defense).
            # So we should pick the top K castles from the available set to defend, where K is the maximum number we can afford.
            # Max K = available - (a[i+1] if i < n-1 else 0).
            # Also K cannot exceed the size of the available set.
            
            # Identify candidates
            candidates = []
            candidates.append(val) # Defend castle i itself
            
            for v in adj[i]:
                candidates.append(c[v])
            
            # Sort candidates descending
            candidates.sort(reverse=True)
            
            # Determine max defenses we can make
            if i < n - 1:
                min_needed_next = a[i+1]
                max_defenses = available - min_needed_next
            else:
                min_needed_next = 0
                max_defenses = available
            
            # We can defend at most max_defenses castles.
            # Also we can't defend more than len(candidates).
            num_defend = min(max_defenses, len(candidates))
            
            # Calculate gain from top num_defend candidates
            gain = sum(candidates[:num_defend])
            
            new_w = available - num_defend
            if new_w > MAX_WARRIORS:
                new_w = MAX_WARRIORS # Should not happen given constraints
            
            if new_dp[new_w] < current_score + gain:
                new_dp[new_w] = current_score + gain
            
            # Update max_reachable
            if new_w > new_max_reachable:
                new_max_reachable = new_w
        
        dp = new_dp
        max_reachable = new_max_reachable
        
        # If no state is reachable, impossible
        if all(x == -1 for x in dp):
            print("-1")
            return

    # After capturing all castles, we want the max score in dp
    ans = 0
    for x in dp:
        if x > ans:
            ans = x
            
    print(ans)

if __name__ == '__main__':
    solve()