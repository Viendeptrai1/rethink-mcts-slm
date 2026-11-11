import sys
from itertools import combinations

def count_unnecessary_cards(N, K, cards):
    # Precompute the sum of all possible subsets
    subset_sums = {}
    for r in range(1, N + 1):
        for subset in combinations(range(N), r):
            subset_sum = sum(cards[i] for i in subset)
            if subset_sum >= K:
                subset_sums[frozenset(subset)] = subset_sum
    
    unnecessary_count = 0
    
    for i in range(N):
        is_unnecessary = True
        for subset, subset_sum in subset_sums.items():
            if i in subset:
                remaining_subset = subset - {i}
                if remaining_subset not in subset_sums or subset_sums[remaining_subset] < K:
                    is_unnecessary = False
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