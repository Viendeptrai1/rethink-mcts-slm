import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    # Sort strings by length
    strings.sort(key=len)
    
    # Initialize result
    result = []
    
    # Use a dictionary to count occurrences of each string
    from collections import defaultdict
    count = defaultdict(int)
    for s in strings:
        count[s] += 1
    
    # Assign 'P' and 'S' based on the count
    for s in strings:
        if count[s] == 1:
            result.append('P')
            count[s] = 0
        else:
            result.append('S')
            count[s] -= 1
    
    # Print the result
    print(''.join(result))

if __name__ == "__main__":
    main()