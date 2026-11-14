import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    N = int(next(iterator))
    
    A = []
    for _ in range(N + 1):
        A.append(int(next(iterator)))
        
    B = []
    for _ in range(N):
        B.append(int(next(iterator)))
        
    total_defeated = 0
    
    # Hero i can attack town i and town i+1
    # We process from left to right (town 1 to town N+1)
    # Hero i is responsible for helping with town i first, then town i+1
    
    # However, the optimal greedy strategy is:
    # For each hero i (from 0 to N-1):
    #   They can help with town i (index i) and town i+1 (index i+1).
    #   But since we process left to right, when we are at hero i, 
    #   town i might still have monsters left that weren't cleared by hero i-1.
    #   Actually, hero i-1 could have helped town i-1 and town i.
    #   So when hero i comes, town i might have remaining monsters.
    #   Hero i should first clear any remaining monsters in town i, then use leftover capacity on town i+1.
    
    # Let's re-simulate:
    # We maintain the remaining monsters for each town.
    # But we don't need to modify A in place if we are careful.
    # Actually, we can simulate the process:
    # For hero i:
    #   They can contribute to town i and town i+1.
    #   But town i might have been partially cleared by hero i-1.
    #   So we need to track how many monsters are left in each town.
    
    # Let's create a copy of A to track remaining monsters
    remaining = list(A)
    
    for i in range(N):
        capacity = B[i]
        
        # First, try to clear remaining monsters in town i (index i)
        if remaining[i] > 0:
            take = min(capacity, remaining[i])
            total_defeated += take
            remaining[i] -= take
            capacity -= take
        
        # If there is still capacity, use it on town i+1 (index i+1)
        if capacity > 0 and i + 1 < len(remaining):
            take = min(capacity, remaining[i+1])
            total_defeated += take
            remaining[i+1] -= take
            capacity -= take
            
    print(total_defeated)

if __name__ == '__main__':
    solve()