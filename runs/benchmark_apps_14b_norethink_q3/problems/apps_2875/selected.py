import sys

def find_reversible_subsequence(n, cards):
    start = -1
    end = -1
    
    # Find the first pair of elements that are out of order
    for i in range(n - 1):
        if cards[i] > cards[i + 1]:
            start = i
            break
    
    # If the array is already sorted
    if start == -1:
        return "impossible"
    
    # Find the last pair of elements that are out of order
    for i in range(n - 1, 0, -1):
        if cards[i] < cards[i - 1]:
            end = i
            break
    
    # Reverse the subsequence between start and end
    cards[start:end+1] = reversed(cards[start:end+1])
    
    # Check if the array is now sorted
    for i in range(n - 1):
        if cards[i] > cards[i + 1]:
            return "impossible"
    
    return f"{start + 1} {end + 1}"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    cards = list(map(int, data[1:]))
    
    result = find_reversible_subsequence(n, cards)
    print(result)

if __name__ == "__main__":
    main()