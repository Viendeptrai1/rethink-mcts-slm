import sys
from collections import defaultdict

def reconstruct_string(s, m, b):
    # Create a list of characters in s sorted by their positions
    sorted_chars = sorted((char, i) for i, char in enumerate(s))
    
    # Initialize the result string t
    t = []
    
    # Dictionary to keep track of used characters
    used = set()
    
    # Process each position in t
    for i in range(m):
        # Find the character that should be placed at position i
        for char, pos in sorted_chars:
            if char not in used:
                # Calculate the potential b value for this character
                potential_b = 0
                for j in range(m):
                    if j != i and ord(t[j]) > ord(char):
                        potential_b += abs(j - i)
                
                # Check if the potential b value matches the required b[i]
                if potential_b == b[i]:
                    t.append(char)
                    used.add(char)
                    break
    
    return ''.join(t)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    q = int(data[index])
    index += 1
    results = []
    
    for _ in range(q):
        s = data[index]
        index += 1
        m = int(data[index])
        index += 1
        b = list(map(int, data[index:index + m]))
        index += m
        
        t = reconstruct_string(s, m, b)
        results.append(t)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()