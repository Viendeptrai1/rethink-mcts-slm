import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    # Create a dictionary to count occurrences of each string
    count_dict = defaultdict(int)
    for s in strings:
        count_dict[s] += 1
    
    # Create a list to store the result
    result = []
    
    # Iterate over the strings and determine if they are prefixes or suffixes
    for s in strings:
        if count_dict[s] == 1:
            # If a string occurs only once, it must be a prefix or suffix
            # We need to determine which one
            # Check if it can be a prefix
            if any(strings[i].startswith(s) for i in range(len(strings))):
                result.append('P')
            else:
                result.append('S')
        else:
            # If a string occurs twice, we need to balance the number of prefixes and suffixes
            # We will assign one as a prefix and the other as a suffix
            if count_dict[s] == 2:
                result.append('P')
                result.append('S')
                count_dict[s] -= 2
    
    # Print the result
    print(''.join(result))

if __name__ == "__main__":
    main()