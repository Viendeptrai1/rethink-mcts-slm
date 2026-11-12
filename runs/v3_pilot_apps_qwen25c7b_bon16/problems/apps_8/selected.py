from collections import Counter

def min_tiles_to_draw(tiles):
    # Count the occurrences of each tile
    count = Counter(tiles)
    
    # Check if there is already a mentsu
    def is_mentsu(count):
        return any(v >= 3 for v in count.values()) or any(count[f'{i}{suit}'] > 0 and count[f'{i+1}{suit}'] > 0 and count[f'{i+2}{suit}'] > 0 for i in range(1, 8) for suit in 'mps')
    
    if is_mentsu(count):
        return 0
    
    # If no mentsu, determine the minimum number of draws needed
    min_draws = float('inf')
    for i in range(1, 10):
        for suit in 'mps':
            new_count = count.copy()
            new_count[f'{i}{suit}'] += 1
            if is_mentsu(new_count):
                min_draws = min(min_draws, 1)
                break
        else:
            continue
        break
    
    for i in range(1, 9):
        for j in range(i+1, 10):
            for suit in 'mps':
                new_count = count.copy()
                new_count[f'{i}{suit}'] += 1
                new_count[f'{j}{suit}'] += 1
                if is_mentsu(new_count):
                    min_draws = min(min_draws, 2)
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    return min_draws

# Read input
tiles = input().split()

# Output the result
print(min_tiles_to_draw(tiles))