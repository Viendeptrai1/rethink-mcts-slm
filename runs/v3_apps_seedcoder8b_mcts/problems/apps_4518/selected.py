def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        a = list(map(int, data[index:index + n]))
        index += n
        
        # Check if it's possible to connect all districts
        from collections import defaultdict, deque
        
        gang_districts = defaultdict(list)
        for i in range(n):
            gang_districts[a[i]].append(i + 1)
        
        # If there's any gang with only one district, it's impossible
        if any(len(districts) == 1 for districts in gang_districts.values()):
            results.append("NO")
            continue
        
        # Otherwise, it's possible to connect all districts
        results.append("YES")
        
        # Create a list of gangs
        gangs = list(gang_districts.keys())
        
        # Connect districts within the same gang
        for gang in gangs:
            districts = gang_districts[gang]
            for i in range(len(districts) - 1):
                results.append(f"{districts[i]} {districts[i + 1]}")
        
        # Connect different gangs
        for i in range(len(gangs) - 1):
            results.append(f"{gang_districts[gangs[i]][0]} {gang_districts[gangs[i + 1]][0]}")
    
    # Print all results
    sys.stdout.write("\n".join(results) + "\n")