import sys
from collections import Counter

def construct_t(s, m, b):
    # Count the frequency of each character in s
    freq = Counter(s)
    
    # Create a list of characters sorted by their frequency in descending order
    sorted_chars = sorted(freq.keys(), key=lambda x: -freq[x])
    
    # Initialize the result string t
    t = []
    
    # Iterate over each character in sorted_chars
    for char in sorted_chars:
        # Find the positions where this character can be placed
        positions = []
        for i in range(m):
            if b[i] == 0:
                positions.append(i)
        
        # Place the character in the positions where it minimizes the b values
        for pos in positions:
            t.insert(pos, char)
            # Update the b values
            for j in range(m):
                if j != pos and t[j] > char:
                    b[j] -= abs(j - pos)
            # Remove the position from the list as it is already used
            positions.remove(pos)
    
    # Join the list into a string and return
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