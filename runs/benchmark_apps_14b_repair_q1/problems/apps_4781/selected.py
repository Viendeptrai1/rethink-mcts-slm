def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    K = int(data[0])
    N = int(data[1])
    
    index = 2
    current_player = K
    total_time = 0
    
    for _ in range(N):
        T = int(data[index])
        Z = data[index + 1]
        index += 2
        
        total_time += T
        
        if total_time >= 210:
            break
        
        if Z == 'T':
            current_player = (current_player % 8) + 1
    
    # Adjust current_player to be within the range 1 to 8
    current_player = (current_player - 1) % 8 + 1
    
    print(current_player)

if __name__ == "__main__":
    main()