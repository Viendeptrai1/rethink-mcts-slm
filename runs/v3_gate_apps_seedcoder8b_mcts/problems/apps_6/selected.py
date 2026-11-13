def min_blows_to_defeat_gorynich(t, queries):
    results = []
    for query in queries:
        n, x = query[0]
        blows = query[1]
        
        # Sort the blows by the effective damage per blow (d_i - h_i)
        # We want to prioritize blows that reduce the number of heads more than they increase it.
        blows.sort(key=lambda blow: (blow[0] - blow[1]), reverse=True)
        
        current_heads = x
        total_blows = 0
        
        for d_i, h_i in blows:
            if current_heads <= 0:
                break
            
            # Calculate how many times we can use this blow before it's no longer beneficial
            times_to_use = (current_heads + h_i - 1) // d_i  # Ceiling division
            
            # Apply the blow
            current_heads -= d_i * times_to_use
            total_blows += times_to_use
            
            # If after using this blow, Gorynich is defeated, we can stop
            if current_heads <= 0:
                results.append(total_blows)
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
        d_i = int(data[index])
        h_i = int(data[index + 1])
        index += 2
        blows.append((d_i, h_i))
    queries.append(((n, x), blows))

# Get results
results = min_blows_to_defeat_gorynich(t, queries)

# Print results
for result in results:
    print(result)