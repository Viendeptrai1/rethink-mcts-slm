import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
sequence = data[1]

# Function to determine if Slavko can win and the best word he can form
def slavko_best_word(N, sequence):
    # Since Mirko always takes the rightmost letter, Slavko will take the leftmost letter each time
    # This means Slavko's word will always be a prefix of the original sequence
    # We need to check if there exists a prefix of sequence that is lexicographically smaller than its complement
    
    # Iterate through all possible prefixes of Slavko's word
    for i in range(1, N + 1):
        slavko_word = sequence[:i]
        mirko_word = sequence[i:]
        
        # Check if slavko_word is lexicographically smaller than mirko_word
        if slavko_word < mirko_word:
            return "DA", slavko_word
        
    # If no such prefix exists, Slavko cannot win
    return "NE", ""

# Get the result and print it
result, best_word = slavko_best_word(N, sequence)
print(result)
if result == "DA":
    print(best_word)