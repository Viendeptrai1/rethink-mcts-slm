def duel_game(n, k, cards):
    if k > n:
        return "once again"

    # Calculate the total possible moves
    total_moves = n - k + 1

    # Check if the total moves exceed 10^9
    if total_moves > 10**9:
        return "once again"

    # Count the number of segments of consecutive '0's and '1's
    segments = []
    current_segment = 1
    
    for i in range(1, n):
        if cards[i] == cards[i - 1]:
            current_segment += 1
        else:
            segments.append(current_segment)
            current_segment = 1
    segments.append(current_segment)
    
    # Check if there's any segment of length at least k
    for segment in segments:
        if segment >= k:
            return "tokitsukaze"
    
    # If no such segment exists, Quailty wins
    return "quailty"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    k = int(data[1])
    cards = data[2]
    result = duel_game(n, k, cards)
    print(result)