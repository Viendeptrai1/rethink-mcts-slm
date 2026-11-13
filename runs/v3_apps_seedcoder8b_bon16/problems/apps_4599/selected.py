def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:N+1]))
    
    # Sort the cards in descending order
    a.sort(reverse=True)
    
    # Alice will take the cards at even indices (0, 2, 4, ...)
    # Bob will take the cards at odd indices (1, 3, 5, ...)
    alice_score = sum(a[i] for i in range(0, N, 2))
    bob_score = sum(a[i] for i in range(1, N, 2))
    
    # Print Alice's score minus Bob's score
    print(alice_score - bob_score)

if __name__ == "__main__":
    main()