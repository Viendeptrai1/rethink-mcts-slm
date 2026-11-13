import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    
    # Count how many times each player answered correctly
    # Players are 1-indexed in input, we'll use 0-indexed internally
    count = [0] * (N + 1)
    
    idx = 3
    for _ in range(Q):
        player = int(data[idx])
        count[player] += 1
        idx += 1
    
    # Initial score is K for everyone
    # If a player answers C times, they gain 0 extra (no bonus mentioned)
    # But every other player loses 1 point for each time someone else answers
    # So if player i answers C_i times:
    # Their score = K - (total answers by others)
    # Total answers by others = Q - C_i
    # Score = K - (Q - C_i) = K - Q + C_i
    
    # Alternatively:
    # Each time someone answers, everyone else loses 1.
    # So after Q total answers, everyone has lost Q points initially.
    # But the person who answered gets +1 relative to others for each of their answers.
    # Base score after all answers without considering own answers: K - Q
    # Then add back the number of times they answered: + count[i]
    # Final score = K - Q + count[i]
    
    total_answers = Q
    base_score = K - total_answers
    
    results = []
    for i in range(1, N + 1):
        final_score = base_score + count[i]
        if final_score > 0:
            results.append("Yes")
        else:
            results.append("No")
    
    for res in results:
        print(res)

if __name__ == "__main__":
    solve()