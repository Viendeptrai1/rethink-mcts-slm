import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_ways_to_arrange_balls(N, K):
    # dp[L][R] will store the number of ways to arrange the first L blue balls followed by R red balls
    # such that Takahashi will need exactly 'move_count' moves to collect all blue balls.
    dp = defaultdict(lambda: [0] * (K + 1))
    
    # Base case: There's only one way to arrange 0 blue and 0 red balls
    dp[(0, 0)][0] = 1

    # Iterate through all possible numbers of blue balls and red balls
    for total_blue in range(K + 1):
        for total_red in range(N - total_blue + 1):
            current_moves = total_red
            current_count = dp[(total_blue, total_red)][current_moves]
            
            if current_count == 0:
                continue
            
            # If we can add another blue ball without increasing the move count
            if total_blue + 1 <= K:
                dp[(total_blue + 1, total_red)][current_moves] = (dp[(total_blue + 1, total_red)][current_moves] + current_count) % MOD
            
            # If we can add a red ball without changing the move count
            if total_red + 1 <= N - total_blue:
                dp[(total_blue, total_red + 1)][current_moves] = (dp[(total_blue, total_red + 1)][current_moves] + current_count) % MOD
            
            # If we can start a new move, i.e., we have collected some blue balls
            if total_blue > 0:
                dp[(total_blue, total_red)][current_moves + 1] = (dp[(total_blue, total_red)][current_moves + 1] + current_count) % MOD

    # Collect results for exactly K blue balls
    result = [dp[(K, N - K)][i] for i in range(1, K + 1)]
    return result

def main():
    input = sys.stdin.read
    data = input().strip()
    N, K = map(int, data.split())
    result = count_ways_to_arrange_balls(N, K)
    for count in result:
        print(count)

if __name__ == "__main__":
    main()