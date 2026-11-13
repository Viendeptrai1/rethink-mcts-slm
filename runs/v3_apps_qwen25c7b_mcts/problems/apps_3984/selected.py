def determine_winner(s):
    n = len(s)
    result = []
    
    for k in range(n):
        if s[k] == 'a':
            result.append('Mike')
        else:
            result.append('Ann')
    
    return result

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    results = determine_winner(s)
    for result in results:
        print(result)