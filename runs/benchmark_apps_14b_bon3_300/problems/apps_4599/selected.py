import sys

def main():
    import sys
    import functools

    def optimal_score_difference(cards):
        @functools.lru_cache(None)
        def dp(i, j):
            if i > j:
                return 0
            # Alice can choose either the i-th or the j-th card
            # She wants to maximize her score minus Bob's score
            return max(cards[i] - dp(i + 1, j), cards[j] - dp(i, j - 1))
        
        return dp(0, len(cards) - 1)

    N = int(sys.stdin.readline())
    cards = list(map(int, sys.stdin.readline().split()))
    result = optimal_score_difference(tuple(cards))
    print(result)

if __name__ == "__main__":
    main()