import sys

def min_lexicographic_string(n, k, s):
    # Count the number of '0's in the string
    zero_count = s.count('0')
    
    # If there are no '0's or k is large enough to sort the entire string
    if zero_count == 0 or k >= n * (n - 1) // 2:
        return ''.join(sorted(s))
    
    # Try to place as many '0's as possible at the beginning
    result = []
    remaining_moves = k
    
    for i in range(n):
        if s[i] == '0':
            if remaining_moves >= i:
                result.append('0')
                remaining_moves -= i
            else:
                break
    
    # Fill the rest of the string with the remaining characters
    remaining_chars = [c for c in s if c not in result]
    result.extend(remaining_chars)
    
    return ''.join(result)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    q = int(data[index])
    index += 1
    results = []
    
    for _ in range(q):
        n = int(data[index])
        k = int(data[index + 1])
        s = data[index + 2]
        index += 3
        
        result = min_lexicographic_string(n, k, s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()