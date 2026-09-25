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
    
    # Assign 'P' and 'S' based on the count of each string
    for s in strings:
        if count_dict[s] == 1:
            result.append('P')
            count_dict[s] = 0
        elif count_dict[s] == 2:
            result.append('S')
            count_dict[s] = 0
    
    # Print the result as a single string
    print(''.join(result))

if __name__ == "__main__":
    solve()