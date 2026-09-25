import sys

def solve():
    import sys
    import random
    
    n = int(sys.stdin.readline())
    friends = list(map(int, sys.stdin.readline().split()))
    
    # Find indices of friends who don't know whom to give the gift to
    unknowns = [i for i in range(n) if friends[i] == 0]
    
    # Create a list of available friends to assign gifts to
    available = [i + 1 for i in range(n) if i + 1 not in friends]
    
    # Randomly assign available friends to unknowns
    random.shuffle(available)
    for i, u in enumerate(unknowns):
        friends[u] = available[i]
    
    # Ensure no friend gives a gift to themselves
    for i in range(n):
        if friends[i] == i + 1:
            # Swap with another friend who is not giving to themselves
            for j in range(n):
                if friends[j] != j + 1 and friends[j] != friends[i]:
                    friends[i], friends[j] = friends[j], friends[i]
                    break
    
    # Print the result
    print(" ".join(map(str, friends)))

if __name__ == "__main__":
    solve()