import sys
input = sys.stdin.read
data = input().split()

def solve_queries(queries):
    results = []
    index = 0
    
    for _ in range(queries):
        n = int(data[index])
        x = int(data[index + 1])
        index += 2
        
        blows = []
        for _ in range(n):
            d = int(data[index])
            h = int(data[index + 1])
            index += 2
            blows.append((d, h))
        
        min_blows = float('inf')
        for blow in blows:
            d, h = blow
            if d >= x:
                min_blows = min(min_blows, 1)
                break
            else:
                needed_heads = x - d
                if needed_heads <= h:
                    min_blows = min(min_blows, 1)
                    break
                else:
                    additional_heads = needed_heads - h
                    total_blows = 1 + additional_heads // d
                    if additional_heads % d != 0:
                        total_blows += 1
                    min_blows = min(min_blows, total_blows)
        
        if min_blows == float('inf'):
            results.append(-1)
        else:
            results.append(min_blows)
    
    return results

# Read input data
t = int(data[0])
queries = [(int(data[i]), int(data[i+1])) for i in range(1, len(data), 2)]
blows_list = [list(map(int, data[i:i+2])) for i in range(t*2+1, len(data), 2)]

# Solve each query
results = solve_queries(t)

# Print results
for result in results:
    print(result)