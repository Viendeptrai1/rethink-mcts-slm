def min_blows_to_defeat_gorynich(t, queries):
    results = []
    for query in queries:
        n, x = query[0]
        blows = query[1]
        
        # Sort the blows by the net gain in heads (h - d) in descending order
        blows.sort(key=lambda blow: blow[1] - blow[0], reverse=True)
        
        # Try to defeat Gorynich using the sorted blows
        current_heads = x
        blow_count = 0
        
        for d, h in blows:
            if current_heads <= 0:
                break
            
            # Calculate how many times we can use this blow
            times = current_heads // d
            
            # If using this blow at least once reduces heads to 0, it's a win
            if times > 0:
                blow_count += 1
                current_heads = max(0, current_heads - d * times + h * times)
            
            # If after using this blow, Gorynich is defeated, we are done
            if current_heads <= 0:
                results.append(blow_count)
                break
        else:
            # If we exit the loop without breaking, it means we couldn't defeat Gorynich
            results.append(-1)
    
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
index = 1
queries = []

for _ in range(t):
    n = int(data[index])
    x = int(data[index + 1])
    index += 2
    blows = []
    for _ in range(n):
        d = int(data[index])
        h = int(data[index + 1])
        index += 2
        blows.append((d, h))
    queries.append(((n, x), blows))

# Get results
results = min_blows_to_defeat_gorynich(t, queries)

# Print results
for result in results:
    print(result)