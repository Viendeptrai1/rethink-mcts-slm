import sys

def find_reversal_interval(cards):
    n = len(cards)
    left = 0
    while left < n - 1 and cards[left] <= cards[left + 1]:
        left += 1
    
    if left == n - 1:
        return "impossible"
    
    right = n - 1
    while right > 0 and cards[right] >= cards[right - 1]:
        right -= 1
    
    if cards[left] <= cards[right + 1] and cards[right] <= cards[left - 1]:
        while left > 0 and cards[left] <= cards[left - 1]:
            left -= 1
        
        while right < n - 1 and cards[right] <= cards[right + 1]:
            right += 1
        
        return f"{left + 1} {right}"
    
    return "impossible"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    cards = list(map(int, data[1:n+1]))
    result = find_reversal_interval(cards)
    print(result)