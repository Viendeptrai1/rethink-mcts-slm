def determine_winner(n, k, cards):
    count_ones = cards.count('1')
    
    if count_ones % 2 == 0:
        if count_ones == 0:
            return "once again"
        else:
            return "quailty"
    else:
        if n - k + 1 >= count_ones:
            return "tokitsukaze"
        else:
            return "once again"

# Main function to handle input and output
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    cards = data[2]
    
    result = determine_winner(n, k, cards)
    print(result)