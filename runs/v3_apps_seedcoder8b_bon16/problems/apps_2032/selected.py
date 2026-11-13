import sys
from heapq import heappop, heappush

def max_importance_of_defended_castles(n, m, k, castles, portals):
    # Prepare portals in an adjacency list
    from collections import defaultdict
    portal_map = defaultdict(list)
    for u, v in portals:
        portal_map[v].append(u)
    
    # Sort portals in decreasing order of u to facilitate processing
    for key in portal_map:
        portal_map[key].sort(reverse=True)

    # Dynamic programming table to track the maximum importance achievable with a given number of warriors
    dp = [-1] * (5001)
    dp[0] = 0  # With 0 warriors, you can't capture any castle

    for i in range(1, n + 1):
        a_i, b_i, c_i = castles[i - 1]
        # We need to capture the i-th castle; hence, dp[i] depends on dp[i-1]
        new_dp = dp[:]
        
        for warriors in range(5001):
            if dp[warriors] == -1 or warriors < a_i:
                continue
            # Capturing the i-th castle
            new_warriors = warriors - a_i + b_i
            if new_warriors <= 5000:
                new_dp[new_warriors] = max(new_dp[new_warriors], dp[warriors] + c_i)
        
        # Now consider using portals to defend the i-th castle
        for warriors in range(5001):
            if dp[warriors] != -1:
                for prev_castle in portal_map[i]:
                    # Use portal from prev_castle to defend i-th castle
                    if warriors > 0:
                        new_warriors = warriors - 1
                        new_dp[new_warriors] = max(new_dp[new_warriors], dp[warriors] + c_i)
        
        dp = new_dp

    # The result is the maximum importance achievable with at least 1 warrior
    result = max(dp[1:])
    return result if result != -1 else -1

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    index = 3
    
    castles = []
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        c_i = int(data[index + 2])
        castles.append((a_i, b_i, c_i))
        index += 3
    
    portals = []
    for _ in range(m):
        u_i = int(data[index])
        v_i = int(data[index + 1])
        portals.append((u_i, v_i))
        index += 2
    
    result = max_importance_of_defended_castles(n, m, k, castles, portals)
    print(result)

if __name__ == "__main__":
    main()