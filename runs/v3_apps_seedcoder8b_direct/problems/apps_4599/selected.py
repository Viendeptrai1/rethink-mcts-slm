def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:N+1]))
    
    # Sort the cards in descending order
    a.sort(reverse=True)
    
    # Alice and Bob take turns, starting with Alice
    alice_score = 0
    bob_score = 0
    
    for i in range(N):
        if i % 2 == 0:
            alice_score += a[i]
        else:
            bob_score += a[i]
    
    # Calculate the difference in scores
    result = alice_score - bob_score
    print(result)

if __name__ == "__main__":
    main()