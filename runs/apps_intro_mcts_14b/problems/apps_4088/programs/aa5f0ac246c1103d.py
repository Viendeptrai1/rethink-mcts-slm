import sys
from collections import defaultdict, deque

def construct_t(s, m, b):
    # Count the frequency of each character in s
    freq = defaultdict(int)
    for char in s:
        freq[char] += 1
    
    # Create a list of characters sorted by their frequency and lexicographical order
    chars = sorted(freq.keys())
    
    # Initialize the result string t
    t = []
    
    # Initialize a queue for each character to keep track of their positions
    queues = {char: deque() for char in chars}
    
    # Fill the queues with positions based on their frequency
    for char in chars:
        for _ in range(freq[char]):
            queues[char].append(len(t))
    
    # Function to calculate the current b value for a given position
    def calculate_b(pos):
        total = 0
        for char in chars:
            while queues[char] and queues[char][0] < pos:
                queues[char].popleft()
            if queues[char]:
                total += abs(pos - queues[char][0])
        return total
    
    # Construct the string t
    for i in range(m):
        # Find the character that minimizes the difference between the current b value and the target b value
        min_diff = float('inf')
        best_char = None
        for char in chars:
            if queues[char]:
                diff = abs(calculate_b(queues[char][0]) - b[i])
                if diff < min_diff:
                    min_diff = diff
                    best_char = char
        
        # Add the best character to the result string
        t.append(best_char)
        
        # Remove the used position from the queue
        queues[best_char].popleft()
    
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
        
        t = construct_t(s, m, b)
        results.append(t)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()