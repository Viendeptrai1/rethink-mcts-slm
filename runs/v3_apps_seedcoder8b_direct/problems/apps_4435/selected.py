from collections import deque

def min_moves_to_opposite_parity(n, a):
    # Initialize the result array with -1
    result = [-1] * n
    # Queues for BFS
    queue = deque()
    visited = [False] * n
    
    # Start BFS from each position
    for i in range(n):
        if not visited[i]:
            queue.append((i, 0))
            visited[i] = True
            
            while queue:
                current, moves = queue.popleft()
                current_value = a[current]
                
                # Check both possible jumps
                for next_pos in (current - current_value, current + current_value):
                    if 0 <= next_pos < n and not visited[next_pos]:
                        # Check if the parity is opposite
                        if (current_value % 2) != (a[next_pos] % 2):
                            result[next_pos] = moves + 1
                            queue.append((next_pos, moves + 1))
                            visited[next_pos] = True
                        else:
                            # If not opposite parity, continue BFS
                            queue.append((next_pos, moves + 1))
                            visited[next_pos] = True
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    result = min_moves_to_opposite_parity(n, a)
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()