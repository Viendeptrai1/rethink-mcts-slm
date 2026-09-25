import sys

def find_string_t(s, m, b):
    # Sort the characters in s by their frequency in descending order
    freq = {}
    for char in s:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    sorted_chars = sorted(freq.keys(), key=lambda x: -freq[x])
    
    # Initialize the result string t
    t = []
    
    # Process each character in the sorted order
    for char in sorted_chars:
        count = freq[char]
        while count > 0:
            # Find the position to insert the current character
            for i in range(m):
                if b[i] == 0:
                    t.append(char)
                    count -= 1
                    break
                else:
                    b[i] -= abs(i + 1 - (len(t) + 1))
    
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
        
        t = find_string_t(s, m, b)
        results.append(t)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()