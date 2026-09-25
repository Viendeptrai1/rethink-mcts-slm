import sys

def main():
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
    
    # Determine which strings are prefixes and which are suffixes
    result = []
    for s in strings:
        if count_dict[s] == 1:
            # If a string appears only once, it must be a prefix or suffix
            # We need to determine which one
            if s in strings[:n-1]:
                result.append('P')
            else:
                result.append('S')
        else:
            # If a string appears twice, we need to balance the number of P's and S's
            # We can assign one as P and the other as S
            if count_dict[s] == 2:
                result.append('P')
                count_dict[s] -= 1
            else:
                result.append('S')
    
    # Print the result
    print(''.join(result))

if __name__ == "__main__":
    main()