import sys

def main():
    import sys
    import bisect
    
    def find_path(n, m, ships):
        # Sort ships by y-coordinate
        ships.sort(key=lambda x: x[2])
        
        # Initialize DP table
        dp = [[float('inf')] * (2 * n + 1) for _ in range(n + 1)]
        dp[0][n] = 0
        
        # Directions: left, straight, right
        directions = [-1, 0, 1]
        
        for t in range(1, n + 1):
            for x in range(-n, n + 1):
                for dx in directions:
                    nx = x + dx
                    if 0 <= nx <= 2 * n:
                        dp[t][nx] = min(dp[t][nx], dp[t - 1][x] + 1)
        
        # Check if we can reach the end without hitting any ship
        for x in range(-n, n + 1):
            if dp[n][x] < float('inf'):
                return "impossible"
        
        # Reconstruct the path
        path = []
        x = n
        for t in range(n, 0, -1):
            for dx in directions:
                nx = x + dx
                if 0 <= nx <= 2 * n and dp[t][x] == dp[t - 1][nx] + 1:
                    path.append('+' if dx == 1 else '-' if dx == -1 else '0')
                    x = nx
                    break
        
        return ''.join(reversed(path))
    
    # Read input
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    ships = []
    index = 2
    for _ in range(m):
        x1 = int(data[index])
        x2 = int(data[index + 1])
        y = int(data[index + 2])
        ships.append((x1, x2, y))
        index += 3
    
    # Find and print the path
    result = find_path(n, m, ships)
    print(result)

if __name__ == "__main__":
    main()