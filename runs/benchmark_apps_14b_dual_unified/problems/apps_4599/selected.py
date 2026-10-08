import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    cards = list(map(int, data[1:]))
    
    cards.sort(reverse=True)
    
    alice_score = sum(cards[0::2])
    bob_score = sum(cards[1::2])
    
    print(alice_score - bob_score)

if __name__ == "__main__":
    main()