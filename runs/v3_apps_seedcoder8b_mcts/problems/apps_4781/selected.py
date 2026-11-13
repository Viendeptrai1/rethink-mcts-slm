def find_exploded_player(K, N, questions):
    players = list(range(1, 9))
    current_index = K - 1
    total_time = 0

    for T, Z in questions:
        total_time += T
        if total_time >= 210:  # 3 minutes and 30 seconds = 210 seconds
            return players[current_index]
        
        if Z == 'T':
            current_index = (current_index + 1) % 8
        elif Z == 'N':
            pass
        elif Z == 'P':
            pass

    return players[current_index]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    K = int(data[0])
    N = int(data[1])
    questions = [(int(data[i]), data[i+1]) for i in range(2, 2 + 2*N, 2)]
    
    result = find_exploded_player(K, N, questions)
    print(result)