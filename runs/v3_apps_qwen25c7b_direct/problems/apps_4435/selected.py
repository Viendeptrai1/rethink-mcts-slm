from collections import deque

def min_moves_to_opposite_parity(n, a):
    result = [-1] * n
    queue = deque()
    
    # Separate positions into two groups based on parity
    odd_positions = [i for i in range(n) if a[i] % 2 == 1]
    even_positions = [i for i in range(n) if a[i] % 2 == 0]
    
    # Initialize distances for odd positions
    for pos in odd_positions:
        queue.append((pos, 0))
        while queue:
            current_pos, current_dist = queue.popleft()
            if a[current_pos] % 2 == 0:
                result[current_pos] = current_dist
                break
            for next_pos in [current_pos - a[current_pos], current_pos + a[current_pos]]:
                if 0 <= next_pos < n and result[next_pos] == -1:
                    queue.append((next_pos, current_dist + 1))
    
    # Reset queue and initialize distances for even positions
    queue.clear()
    for pos in even_positions:
        queue.append((pos, 0))
        while queue:
            current_pos, current_dist = queue.popleft()
            if a[current_pos] % 2 == 1:
                result[current_pos] = current_dist
                break
            for next_pos in [current_pos - a[current_pos], current_pos + a[current_pos]]:
                if 0 <= next_pos < n and result[next_pos] == -1:
                    queue.append((next_pos, current_dist + 1))
    
    return result

# Example usage
n = int(input())
a = list(map(int, input().split()))
print(" ".join(map(str, min_moves_to_opposite_parity(n, a))))