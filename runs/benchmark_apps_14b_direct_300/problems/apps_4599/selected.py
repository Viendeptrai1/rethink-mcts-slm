import sys

def main():
    import sys
    import functools

    def optimal_score(cards):
        @functools.lru_cache(None)
        def dp(i, j):
            if i > j:
                return 0
            if i == j:
                return cards[i]
            return max(cards[i] + dp(i + 1, j), cards[j] + dp(i, j - 1))
        
        n = len(cards)
        total_sum = sum(cards)
        alice_score = dp(0, n - 1)
        bob_score = total_sum - alice_score
        return alice_score - bob_score

    def read_input():
        input = sys.stdin.read
        data = input().split()
        N = int(data[0])
        cards = list(map(int, data[1:]))
        return N, cards

    N, cards = read_input()
    result = optimal_score(cards)
    print(result)

if __name__ == "__main__":
    main()