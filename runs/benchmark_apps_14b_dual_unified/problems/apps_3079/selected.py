import sys

def can_slavko_win_and_best_word(N, sequence):
    mirko_word = []
    slavko_word = []
    
    # Mirko always takes the rightmost letter
    # Slavko needs to form the lexicographically smallest word possible
    for i in range(N // 2):
        # Mirko's turn
        mirko_word.append(sequence.pop())
        
        # Slavko's turn
        slavko_word.append(sequence.pop())
    
    # After all turns, check if Slavko's word is lexicographically smaller
    if ''.join(slavko_word) < ''.join(mirko_word):
        return "DA", ''.join(slavko_word)
    else:
        return "NE", ''.join(slavko_word)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    sequence = list(data[1])
    
    result, best_word = can_slavko_win_and_best_word(N, sequence)
    print(result)
    print(best_word)

if __name__ == "__main__":
    main()