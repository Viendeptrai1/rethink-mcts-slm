import sys

def find_reversible_subsequence(n, cards):
    # Find the first and last positions where the order is violated
    start = -1
    end = -1
    
    for i in range(n - 1):
        if cards[i] > cards[i + 1]:
            if start == -1:
                start = i
            end = i + 1
    
    # If the array is already sorted or has only one inversion
    if start == -1:
        return "impossible"
    
    # Check if reversing the subarray from start+1 to end fixes the array
    reversed_cards = cards[:start] + cards[start:end+1][::-1] + cards[end+1:]
    
    for i in range(n - 1):
        if reversed_cards[i] > reversed_cards[i + 1]:
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