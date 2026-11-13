from collections import defaultdict, deque

def can_connect_districts(n, gangs):
    gang_count = defaultdict(int)
    for g in gangs:
        gang_count[g] += 1
    
    # Check if there exists at least one gang with more than one district
    for count in gang_count.values():
        if count > 1:
            return "NO", []
    
    # If all gangs have only one district, we can connect them in a chain
    result = []
    for i in range(1, n):
        result.append((i, i + 1))
    
    return "YES", result

def main():
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
        gangs = list(map(int, data[index:index + n]))
        index += n
        
        result_type, roads = can_connect_districts(n, gangs)
        results.append(result_type)
        if result_type == "YES":
            results.extend([f"{x} {y}" for x, y in roads])
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()