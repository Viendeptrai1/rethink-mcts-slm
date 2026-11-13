def find_exploder_player(K, N, questions):
    players = list(range(1, 9))
    current_index = K - 1

    for time, outcome in questions:
        if outcome == 'T':
            current_index = (current_index + 1) % len(players)
        elif outcome == 'N':
            pass
        elif outcome == 'P':
            pass

    return players[current_index]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    K = int(data[0])
    N = int(data[1])
    questions = [tuple(data[i].split()) for i in range(2, 2 + N)]
    questions = [(int(T), Z) for T, Z in questions]
    
    result = find_exploder_player(K, N, questions)
    print(result)