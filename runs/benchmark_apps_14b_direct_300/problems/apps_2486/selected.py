import sys
from itertools import combinations

def count_unnecessary_cards(N, K, cards):
    def is_good_subset(subset):
        return sum(subset) >= K

    unnecessary_count = 0

    for i in range(N):
        card_i = cards[i]
        remaining_cards = cards[:i] + cards[i+1:]
        
        # Check if removing card_i makes any good subset bad
        is_unnecessary = True
        for r in range(1, len(remaining_cards) + 1):
            for subset in combinations(remaining_cards, r):
                if is_good_subset(subset) and not is_good_subset(subset + (card_i,)):
                    is_unnecessary = False
                    break
            if not is_unnecessary:
                break
        
        if is_unnecessary:
            unnecessary_count += 1

    return unnecessary_count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    cards = list(map(int, data[2:]))
    
    result = count_unnecessary_cards(N, K, cards)
    print(result)

if __name__ == "__main__":
    main()