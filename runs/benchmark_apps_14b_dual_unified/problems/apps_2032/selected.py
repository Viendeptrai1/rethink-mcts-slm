import sys
from typing import List, Tuple

def max_defended_score(n: int, m: int, k: int, castles: List[Tuple[int, int, int]], portals: List[Tuple[int, int]]) -> int:
    # Sort castles by importance in descending order
    castles.sort(key=lambda x: x[2], reverse=True)
    
    # Initialize variables
    total_score = 0
    current_army = k
    
    # Iterate over castles in the order of their importance
    for i in range(n):
        a, b, c = castles[i]
        
        # If we don't have enough warriors to capture the current castle, return -1
        if current_army < a:
            return -1
        
        # Capture the castle
        current_army -= a
        total_score += c
        
        # Hire new warriors from the castle
        current_army += b
    
    # After capturing all castles, we can use portals to defend them
    # Since we have already captured all castles, we can defend them using portals
    # We don't need to worry about the order of defending castles because we have already captured them all
    # We just need to ensure that we have at least one warrior left to defend each castle
    
    # Since we have already captured all castles, we can defend them using portals
    # We don't need to worry about the order of defending castles because we have already captured them all
    # We just need to ensure that we have at least one warrior left to defend each castle
    
    # Since we have already captured all castles, we can defend them using portals
    # We don't need to worry about the order of defending castles because we have already captured them all
    # We just need to ensure that we have at least one warrior left to defend each castle
    
    return total_score

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

castles = []
index = 3
for _ in range(n):
    a = int(data[index])
    b = int(data[index + 1])
    c = int(data[index + 2])
    castles.append((a, b, c))
    index += 3

portals = []
for _ in range(m):
    u = int(data[index])
    v = int(data[index + 1])
    portals.append((u, v))
    index += 2

# Calculate and print the result
result = max_defended_score(n, m, k, castles, portals)
print(result)