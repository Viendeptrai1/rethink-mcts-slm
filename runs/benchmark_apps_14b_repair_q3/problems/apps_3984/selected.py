def determine_winner(s):
    n = len(s)
    winners = []
    
    # Create an array to store the smallest suffix starting from each position
    smallest_suffix = [0] * n
    
    # Initialize the smallest suffix for the last character
    smallest_suffix[n - 1] = n - 1
    
    # Fill the smallest_suffix array from right to left
    for i in range(n - 2, -1, -1):
        if s[i] <= s[smallest_suffix[i + 1]]:
            smallest_suffix[i] = i
        else:
            smallest_suffix[i] = smallest_suffix[i + 1]
    
    # Determine the winner for each k
    for k in range(n):
        if k == smallest_suffix[k]:
            winners.append('Mike')
        else:
            winners.append('Ann')
    
    return winners

def main():
    import sys
    s = sys.stdin.read().strip()
    winners = determine_winner(s)
    for winner in winners:
        print(winner)

if __name__ == "__main__":
    main()