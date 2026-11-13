import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    N = int(data[idx])
    idx += 1
    
    A = []
    for _ in range(N + 1):
        A.append(int(data[idx]))
        idx += 1
    
    B = []
    for _ in range(N):
        B.append(int(data[idx]))
        idx += 1
    
    # Greedy approach:
    # Process towns from left to right.
    # For town i (0-indexed), we have A[i] monsters.
    # Hero i-1 (if exists) can help with town i-1 and i. We already decided how much hero i-1 used for town i-1.
    # Hero i can help with town i and i+1.
    # Strategy: For town i, first use any remaining capacity from hero i-1 (if any).
    # Then, use hero i's capacity to cover the remaining monsters at town i.
    # The key insight is that hero i's capacity can be split between town i and i+1.
    # To maximize total, we should prioritize covering monsters at town i using hero i, 
    # because hero i-1's capacity for town i is "wasted" if not used, and hero i's capacity 
    # is the only one that can cover town i+1. However, a better greedy strategy is:
    # Iterate i from 0 to N-1 (representing heroes).
    # Hero i can cover town i and town i+1.
    # We should use hero i to cover as much as possible of town i first? 
    # Actually, consider the flow:
    # Town 0: only Hero 0 can help.
    # Town 1: Hero 0 and Hero 1 can help.
    # ...
    # Town i: Hero i-1 and Hero i can help.
    #
    # Optimal Greedy:
    # Iterate through towns from 0 to N.
    # For town i, we have A[i] monsters.
    # We can use leftover capacity from Hero i-1 (which was intended for town i-1 but might have overflowed? No, capacity is limited).
    # Let's reframe:
    # Let's iterate through heroes i from 0 to N-1.
    # Hero i has capacity B[i].
    # Town i has A[i] monsters. Town i+1 has A[i+1] monsters.
    # Hero i can contribute to town i and town i+1.
    # But town i can also be helped by Hero i-1.
    #
    # Correct Greedy Logic:
    # Process from left to right (town 0 to N).
    # Maintain the remaining capacity of the previous hero (hero i-1) that was not used for town i-1.
    # Actually, it's simpler:
    # For town i, the monsters can be defeated by Hero i-1 (if i>0) or Hero i.
    # Hero i-1's capacity was primarily for town i-1, but any unused capacity can be used for town i.
    # Hero i's capacity is for town i and i+1.
    # To maximize, when at town i:
    # 1. Use any remaining capacity from Hero i-1 to defeat monsters at town i.
    # 2. If monsters remain, use Hero i's capacity to defeat them.
    # 3. The rest of Hero i's capacity (if any) is carried over to help town i+1.
    #
    # Wait, is this optimal?
    # Suppose A = [10, 10], B = [10, 10].
    # Town 0: 10 monsters. Hero 0 has 10. Use 10 for Town 0. Hero 0 left: 0.
    # Town 1: 10 monsters. Hero 0 left: 0. Hero 1 has 10. Use 10 for Town 1. Total 20. Correct.
    #
    # Suppose A = [5, 10, 5], B = [10, 10].
    # Town 0: 5 monsters. Hero 0 has 10. Use 5. Hero 0 left: 5.
    # Town 1: 10 monsters. Hero 0 left: 5. Use 5. Remaining: 5. Hero 1 has 10. Use 5. Hero 1 left: 5.
    # Town 2: 5 monsters. Hero 1 left: 5. Use 5. Total: 5+10+5 = 20. Correct.
    #
    # Is there a case where using Hero i-1 for town i is bad?
    # Hero i-1 can ONLY help town i-1 and i. If we don't use it for town i, it's wasted (since town i-1 is already processed).
    # Hero i can help town i and i+1. If we use it for town i, it reduces capacity for i+1.
    # However, town i MUST be covered. The only sources are Hero i-1 and Hero i.
    # Hero i-1's capacity for town i is "expiring" after town i.
    # Hero i's capacity for town i is shared with town i+1.
    # If we have excess capacity from Hero i-1, we MUST use it on town i, otherwise it's lost forever.
    # If we don't have enough from Hero i-1, we MUST use Hero i.
    # The only trade-off is: if Hero i has plenty, should we save some for town i+1?
    # Yes, but we only use what is necessary for town i. We don't use more than needed for town i.
    # So the greedy strategy holds:
    # For each town i from 0 to N:
    #   current_monsters = A[i]
    #   if i > 0:
    #       use = min(current_monsters, prev_hero_remaining)
    #       current_monsters -= use
    #       prev_hero_remaining -= use
    #   if current_monsters > 0:
    #       use = min(current_monsters, current_hero_capacity)
    #       current_monsters -= use
    #       current_hero_remaining = current_hero_capacity - use
    #       total_defeated += (A[i] - current_monsters)
    #
    # Wait, the logic above for "current_hero_remaining" needs to be passed to the next iteration.
    # Let's refine variables.
    
    total_defeated = 0
    prev_hero_remaining = 0  # Capacity left from Hero i-1 after helping town i-1
    
    # We iterate through towns 0 to N.
    # For town i, the relevant heroes are:
    # - Hero i-1 (if i>0): has 'prev_hero_remaining' capacity.
    # - Hero i (if i<N): has B[i] capacity.
    
    for i in range(N + 1):
        monsters = A[i]
        
        # First, use leftover from previous hero
        if i > 0:
            use = min(monsters, prev_hero_remaining)
            monsters -= use
            prev_hero_remaining -= use
        
        # Then, use current hero's capacity
        if i < N:
            use = min(monsters, B[i])
            monsters -= use
            # The remaining capacity of current hero becomes the 'prev_hero_remaining' for the next town (i+1)
            prev_hero_remaining = B[i] - use
        
        total_defeated += (A[i] - monsters)
        
        # If monsters > 0, they are not defeated.
    
    print(total_defeated)

if __name__ == '__main__':
    solve()