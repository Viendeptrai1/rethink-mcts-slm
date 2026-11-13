def solve():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    N = int(data[0])
    sequence = data[1]
    
    # Slavko always takes the rightmost letter
    slavko_word = sequence[::-1]
    
    # Determine if Slavko can win
    # If the sequence length is even, Slavko can always mirror the sequence
    # and Mirko will always have a lexicographically smaller word.
    # If the sequence length is odd, Slavko can mirror the sequence and
    # still have a lexicographically larger word than Mirko's.
    
    if N % 2 == 0:
        print("NE")
    else:
        print("DA")
    
    # Output the most beautiful word Slavko can have
    print(slavko_word)