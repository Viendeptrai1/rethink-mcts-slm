from collections import deque
import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    # Initialize the result array with -1
    d = [-1] * n
    
    # Queue for BFS
    queue = deque()
    
    # Start BFS from each position
    for i in range(n):
        if d[i] == -1:  # If not visited
            queue.append((i, 0))  # (position, distance)
            d[i] = 0  # Distance to itself is 0
            
            while queue:
                current, dist = queue.popleft()
                
                # Check the two possible jumps
                for next_pos in (current - a[current], current + a[current]):
                    if 0 <= next_pos < n and d[next_pos] == -1:
                        # Check for opposite parity
                        if (a[current] % 2) != (a[next_pos] % 2):
                            d[next_pos] = dist + 1
                            queue.append((next_pos, dist + 1))
                        else:
                            # If same parity, continue BFS without increasing distance
                            queue.append((next_pos, dist))
    
    # Print the result
    print(" ".join(map(str, d)))