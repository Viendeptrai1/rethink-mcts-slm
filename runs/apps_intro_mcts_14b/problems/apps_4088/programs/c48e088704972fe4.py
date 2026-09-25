import sys
from collections import deque

def reconstruct_string(s, m, b):
    # Sort characters in s by their frequency in descending order
    char_count = {}
    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    sorted_chars = sorted(char_count.keys(), key=lambda x: -char_count[x])
    
    # Initialize the result string t and a queue for characters
    t = []
    char_queue = deque()
    
    # Process each character in the sorted order
    for char in sorted_chars:
        while char_queue and b and b[-1] == 0:
            t.append(char_queue.popleft())
        
        if b:
            t.append(char)
            b.pop(0)
        
        char_queue.append(char)
    
    # Append remaining characters from the queue to t
    while char_queue:
        t.append(char_queue.popleft())
    
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