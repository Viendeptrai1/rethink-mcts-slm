import sys

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    # Create a dictionary to count occurrences of each string
    count_dict = {}
    for s in strings:
        if s in count_dict:
            count_dict[s] += 1
        else:
            count_dict[s] = 1
    
    # Create a list of tuples (string, count)
    string_count = [(s, count_dict[s]) for s in strings]
    
    # Sort the list by string length
    string_count.sort(key=lambda x: len(x[0]))
    
    # Initialize the result string
    result = []
    
    # Process each length from 1 to n-1
    for length in range(1, n):
        # Find the two strings of this length
        candidates = [s for s, count in string_count if len(s) == length]
        
        # Assign one as prefix and the other as suffix
        result.append('P')
        result.append('S')
        
        # Remove these strings from the list
        string_count.remove((candidates[0], 1))
        string_count.remove((candidates[1], 1))
    
    # Print the result
    print(''.join(result))

if __name__ == "__main__":
    solve()