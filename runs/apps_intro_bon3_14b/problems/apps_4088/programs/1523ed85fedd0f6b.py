import sys
from collections import deque

def reconstruct_string(s, m, b):
    # Create a list of characters in s sorted by their positions
    sorted_chars = sorted((char, i) for i, char in enumerate(s))
    
    # Initialize the result string t
    t = []
    
    # Use a deque to efficiently pop elements from the end
    available_chars = deque(sorted_chars)
    
    # Process each position in t
    for i in range(m):
        # Find the character that fits the current position
        while available_chars and available_chars[-1][1] < i + b[i]:
            available_chars.pop()
        
        # The character at the front of the deque is the one we need
        char, pos = available_chars.popleft()
        t.append(char)
    
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