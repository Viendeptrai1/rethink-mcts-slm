import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # Mirko takes indices: n-1, n-3, n-5, ...
    # Slavko takes indices: n-2, n-4, n-6, ...
    
    mirko_chars = []
    slavko_chars = []
    
    for i in range(n - 1, -1, -2):
        mirko_chars.append(s[i])
    
    for i in range(n - 2, -1, -2):
        slavko_chars.append(s[i])
    
    # Sort both to get the most beautiful (lexicographically smallest) words
    mirko_word = "".join(sorted(mirko_chars))
    slavko_word = "".join(sorted(slavko_chars))
    
    # Compare words
    if slavko_word < mirko_word:
        print("DA")
        print(slavko_word)
    else:
        print("NE")
        print(slavko_word)

if __name__ == "__main__":
    solve()