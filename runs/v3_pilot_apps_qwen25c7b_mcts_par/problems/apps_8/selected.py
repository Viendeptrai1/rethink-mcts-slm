from collections import Counter

def min_tiles_to_draw(hand):
    def is_mentsu(hand):
        count = Counter(hand)
        for i in range(7):
            if count[f'{i+1}m'] >= 3 or count[f'{i+1}p'] >= 3 or count[f'{i+1}s'] >= 3:
                return True
            if (count[f'{i+1}m'] >= 1 and count[f'{i+2}m'] >= 1 and count[f'{i+3}m'] >= 1 or
                count[f'{i+1}p'] >= 1 and count[f'{i+2}p'] >= 1 and count[f'{i+3}p'] >= 1 or
                count[f'{i+1}s'] >= 1 and count[f'{i+2}s'] >= 1 and count[f'{i+3}s'] >= 1):
                return True
        return False

    if is_mentsu(hand):
        return 0
    
    for i in range(1, 10):
        for suit in 'mps':
            new_hand = hand + [f'{i}{suit}']
            if is_mentsu(new_hand):
                return 1
    
    return 2

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
print(min_tiles_to_draw(data))