import sys
from collections import defaultdict

def solve(s, m, b):
    # Create a list of positions for each character in s
    pos = defaultdict(list)
    for i, c in enumerate(s):
        pos[c].append(i)
    
    # Sort the positions for each character
    for c in pos:
        pos[c].sort()
    
    # Initialize the result string
    t = []
    
    # Process each position in b
    for i in range(m):
        # Find the character that should be at position i in t
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if not pos[c]:
                continue
            
            # Calculate the sum of distances for the current character
            total_distance = 0
            for j in pos[c]:
                if j < i:
                    total_distance += i - j
                else:
                    total_distance += j - i
            
            # Check if the total distance matches b[i]
            if total_distance == b[i]:
                # Add the character to the result
                t.append(c)
                # Remove the used position from the list
                pos[c].pop(0)
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