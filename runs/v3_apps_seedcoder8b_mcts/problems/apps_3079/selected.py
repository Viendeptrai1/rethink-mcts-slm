def solve():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    N = int(data[0])
    sequence = data[1]
    
    # Slavko always takes the rightmost letter
    slavko_word = sequence[::-1]
    
    # Determine if Slavko can win
    # If the sequence length is even, Slavko can always rearrange his letters
    # to be more beautiful than Mirko's word, which is just the sorted sequence.
    if N % 2 == 0:
        print("DA")
    else:
        print("NE")
    
    # Output the most beautiful word Slavko can have
    print(slavko_word)