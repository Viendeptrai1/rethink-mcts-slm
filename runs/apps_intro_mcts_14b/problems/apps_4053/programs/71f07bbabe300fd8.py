import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    # Create a dictionary to store the count of each string
    string_count = defaultdict(int)
    for s in strings:
        string_count[s] += 1
    
    # Create a list to store the result
    result = []
    
    # Iterate over the strings and determine if they are prefixes or suffixes
    for s in strings:
        if string_count[s] == 1:
            # If the string appears only once, it must be a prefix or suffix
            # Check if it can be a prefix
            if any(s + t in strings for t in strings):
                result.append('P')
            else:
                result.append('S')
        else:
            # If the string appears twice, we need to check its compatibility
            # Find the other occurrence of the string
            other_index = strings.index(s, strings.index(s) + 1)
            other_string = strings[other_index]
            
            # Check if they can form a valid prefix and suffix
            if s + other_string in strings or other_string + s in strings:
                result.append('P')
                result.append('S')
            else:
                result.append('S')
                result.append('P')
        
        # Remove the string from the dictionary to avoid counting it again
        string_count[s] -= 1
    
    # Print the result
    print(''.join(result))

if __name__ == "__main__":
    main()