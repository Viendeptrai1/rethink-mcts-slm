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
    
    # Initialize the result list
    result = []
    
    # Iterate over the strings and determine if they are prefixes or suffixes
    for s in strings:
        if count_dict[s] == 1:
            # If a string appears only once, it must be a prefix or suffix
            # Check if it can be a prefix
            if strings.count(s + s[0]) > 0:
                result.append('P')
            else:
                result.append('S')
        else:
            # If a string appears twice, we need to check compatibility
            # Find the other occurrence of the string
            other_index = strings.index(s, strings.index(s) + 1)
            # Check if they can form a valid prefix and suffix combination
            if strings.index(s) < other_index:
                result.append('P')
                result.append('S')
            else:
                result.append('S')
                result.append('P')
    
    # Print the result
    print(''.join(result))

if __name__ == "__main__":
    solve()