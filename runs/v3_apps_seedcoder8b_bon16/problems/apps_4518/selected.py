def solve():
    import sys
    input = sys.stdin.readline

    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        a = list(map(int, input().strip().split()))
        
        gang_groups = {}
        for i, gang in enumerate(a):
            if gang not in gang_groups:
                gang_groups[gang] = []
            gang_groups[gang].append(i + 1)
        
        if len(gang_groups) == 1:
            # If all districts are in one gang, it's impossible
            print("NO")
            continue
        
        # If there are at least two gangs, we can connect them all
        roads = []
        
        # Take two different gangs
        gang1, gang2 = list(gang_groups.keys())[:2]
        roads.append((gang_groups[gang1][0], gang_groups[gang2][0]))
        
        # Connect remaining districts in the first gang
        for i in range(1, len(gang_groups[gang1])):
            roads.append((gang_groups[gang1][i], roads[-1][1]))
        
        # Connect remaining districts in the second gang
        for i in range(1, len(gang_groups[gang2])):
            roads.append((gang_groups[gang2][i], roads[-1][1]))
        
        # Output the result
        print("YES")
        for x, y in roads:
            print(x, y)