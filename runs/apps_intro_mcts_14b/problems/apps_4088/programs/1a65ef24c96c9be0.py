import sys
from collections import deque

def reconstruct_string(s, m, b):
    # Sort characters by their frequency in descending order
    freq = [0] * 26
    for char in s:
        freq[ord(char) - ord('a')] += 1
    
    sorted_chars = sorted([(chr(i + ord('a')), freq[i]) for i in range(26)], key=lambda x: x[1], reverse=True)
    
    # Initialize the result string and a deque to keep track of positions
    t = []
    positions = deque()
    
    # Process each character in the sorted list
    for char, _ in sorted_chars:
        while b and b[-1] == 0:
            t.append(b.pop())
            positions.append(len(t))
        
        if not b:
            break
        
        # Find the correct position for the current character
        pos = len(t)
        while pos > 0 and b[pos - 1] >= pos:
            pos -= 1
        
        # Insert the character at the found position
        t.insert(pos, char)
        positions.appendleft(pos)
        
        # Update the b values
        for i in range(len(t)):
            if t[i] > char:
                b[i] -= abs(i - pos)
    
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
        
        result = reconstruct_string(s, m, b)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()