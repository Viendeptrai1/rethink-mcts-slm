import sys
import functools

def main():
    def optimal_score(cards):
        @functools.lru_cache(None)
        def dp(i, j):
            if i > j:
                return 0
            if i == j:
                return cards[i]
            # Alice can choose either the leftmost or the rightmost card
            # She wants to maximize her score minus Bob's score
            return max(cards[i] - dp(i + 1, j), cards[j] - dp(i, j - 1))
        
        return dp(0, len(cards) - 1)

    N = int(sys.stdin.readline())
    cards = list(map(int, sys.stdin.readline().split()))
    result = optimal_score(cards)
    print(result)

if __name__ == "__main__":
    main()