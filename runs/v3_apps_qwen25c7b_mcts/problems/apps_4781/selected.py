def find_exploding_player(K, N, questions):
    players = list(range(1, 9))
    current_index = players.index(K)
    
    for _, answer in questions:
        if answer == 'N' or answer == 'P':
            continue
        else:
            current_index = (current_index + 1) % len(players)
    
    return players[current_index]

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    K = int(data[0])
    N = int(data[1])
    questions = [(int(data[i*2+2]), data[i*2+3]) for i in range(N)]
    
    result = find_exploding_player(K, N, questions)
    print(result)