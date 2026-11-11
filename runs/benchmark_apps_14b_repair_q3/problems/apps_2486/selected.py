import sys
from itertools import combinations

def count_unnecessary_cards(N, K, cards):
    unnecessary_count = 0
    necessary_cards = set()
    
    # Check all subsets of cards
    for r in range(1, N + 1):
        for subset in combinations(cards, r):
            if sum(subset) >= K:
                # Check if removing each card in the subset results in a good subset
                for i in range(r):
                    if sum(subset[:i] + subset[i+1:]) < K:
                        break
                else:
                    # If we didn't break, all cards in this subset are unnecessary
                    for card in subset:
                        necessary_cards.add(card)
    
    # The number of unnecessary cards is the total number of cards minus the number of necessary cards
    unnecessary_count = N - len(necessary_cards)
    
    return unnecessary_count

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    cards = list(map(int, data[2:]))
    
    result = count_unnecessary_cards(N, K, cards)
    print(result)

if __name__ == "__main__":
    main()