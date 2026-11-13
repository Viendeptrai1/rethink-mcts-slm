def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    moves = data[1]
    
    def count_glasses(n, moves):
        glasses = 0
        m = len(moves)
        
        # Iterate over each turn
        for i in range(m):
            # The current player index
            current_index = i % n
            # Check if the current player is Vasya (index 0)
            if current_index == 0:
                # The action on this turn
                action = moves[i]
                
                # Determine the last three moves for Vasya
                if i >= 3:
                    prev_actions = moves[i-3:i]
                else:
                    prev_actions = moves[:i]
                
                # Check if Vasya made the same moves in the last 3 turns
                if len(set(prev_actions)) == 1 and len(prev_actions) == 3:
                    # If yes, Vasya drinks a glass
                    glasses += 1
                    # Skip the next turn as the game goes to the next person
                    if i + 1 < m:
                        i += 1
        
        return glasses
    
    print(count_glasses(n, moves))

if __name__ == "__main__":
    main()