import sys
from collections import defaultdict

def solve(s, m, b):
    # Create a list of characters in s sorted by their positions
    sorted_chars = sorted((char, i) for i, char in enumerate(s))
    
    # Create a dictionary to store the positions of each character
    char_positions = defaultdict(list)
    for char, pos in sorted_chars:
        char_positions[char].append(pos)
    
    # Initialize the result string t
    t = []
    
    # Process each position in b
    for i in range(m):
        # Find the character that should be at position i in t
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char_positions[char]:
                # Calculate the sum of distances for the current character
                current_sum = 0
                for j in range(m):
                    if j != i and char_positions[char] and char_positions[char][0] < char_positions[s[j]][0]:
                        current_sum += abs(i - j)
                
                # If the current sum matches b[i], add the character to t
                if current_sum == b[i]:
                    t.append(char)
                    char_positions[char].pop(0)
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
        
        result = solve(s, m, b)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()