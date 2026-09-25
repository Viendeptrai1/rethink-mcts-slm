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
    
    # Create a list to store the result
    result = []
    
    # Iterate over the strings and determine if they are prefixes or suffixes
    for s in strings:
        if count_dict[s] == 1:
            # If a string appears only once, it must be a prefix or suffix
            # Check if it can be a prefix
            if any(s + t for t in strings if len(s + t) == n):
                result.append('P')
            else:
                result.append('S')
        else:
            # If a string appears twice, it can be either a prefix or a suffix
            # We need to check the context to determine its role
            # For simplicity, we assume the first occurrence is a prefix and the second is a suffix
            result.append('P')
            count_dict[s] -= 1
    
    # Print the result
    print(''.join(result))

if __name__ == "__main__":
    solve()