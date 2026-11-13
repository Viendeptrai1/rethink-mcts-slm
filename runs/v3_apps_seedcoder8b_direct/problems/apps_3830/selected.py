def count_returnable_rooms(t, test_cases):
    results = []
    for n, s in test_cases:
        # Initialize a list to track reachability
        reachable = [False] * n
        
        # Check reachability for each room
        for start in range(n):
            # Try to find a cycle starting from room `start`
            current = start
            visited = set()
            while current not in visited:
                visited.add(current)
                if s[current] == '>':
                    current = (current + 1) % n
                elif s[current] == '<':
                    current = (current - 1 + n) % n
                else:  # s[current] == '-'
                    # If belt is off, we can go either way
                    # Try both directions
                    forward = (current + 1) % n
                    backward = (current - 1 + n) % n
                    if forward not in visited:
                        current = forward
                    elif backward not in visited:
                        current = backward
                    else:
                        break
            
            # If we returned to the start, mark all visited rooms as reachable
            if current == start:
                for room in visited:
                    reachable[room] = True
        
        # Count the number of reachable rooms
        returnable_count = sum(reachable)
        results.append(returnable_count)
    
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
index = 1
test_cases = []
for _ in range(t):
    n = int(data[index])
    s = data[index + 1]
    test_cases.append((n, s))
    index += 2

# Get results
results = count_returnable_rooms(t, test_cases)

# Print results
for result in results:
    print(result)