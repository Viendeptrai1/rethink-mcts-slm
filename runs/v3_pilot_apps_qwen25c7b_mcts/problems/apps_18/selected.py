import heapq

def min_lexicographical_string(s):
    t = []
    u = []
    
    # Push all characters of s into the heap t
    for char in s:
        heapq.heappush(t, char)
    
    # Process the heap to form the minimal lexicographical string u
    while t:
        # Pop the smallest character from t
        smallest_char = heapq.heappop(t)
        # Append it to u
        u.append(smallest_char)
    
    # Join the list u into a string and return it
    return ''.join(u)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    result = min_lexicographical_string(s)
    print(result)