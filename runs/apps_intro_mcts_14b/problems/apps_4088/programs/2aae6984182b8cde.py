import sys
from collections import defaultdict

def solve(s, m, b):
    n = len(s)
    # Create a list of positions for each character
    positions = defaultdict(list)
    for i, char in enumerate(s):
        positions[char].append(i)
    
    # Sort the characters by their lexicographical order
    sorted_chars = sorted(positions.keys())
    
    # Initialize the result string
    t = []
    
    # Process each character in the sorted order
    for char in sorted_chars:
        pos_list = positions[char]
        while pos_list:
            # Find the best position to place the current character
            best_pos = None
            best_score = float('inf')
            for pos in pos_list:
                score = 0
                for j in range(m):
                    if b[j] == 0:
                        continue
                    if ord(t[j]) < ord(char):
                        score += abs(j - pos)
                if score < best_score:
                    best_score = score
                    best_pos = pos
            # Place the character in the best position
            t.append(char)
            pos_list.remove(best_pos)
            # Update the b array
            for j in range(m):
                if b[j] == 0:
                    continue
                if ord(t[j]) < ord(char):
                    b[j] -= abs(j - best_pos)
    
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