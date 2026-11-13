def max_segments(n, k, a):
    # Convert each number to binary representation and pad with leading zeros
    a = [format(x, f'0{k}b') for x in a]
    
    # Function to flip a bit at position j in string s
    def flip(s, j):
        return s[:j] + ('0' if s[j] == '1' else '1') + s[j+1:]
    
    # Initialize variables
    result = 0
    current_segment = ''
    
    # Iterate through the array to form segments
    for num in a:
        if current_segment == '':
            current_segment = num
            result += 1
        elif current_segment != num:
            current_segment = num
            result += 1
        else:
            # Flip a bit to create a new segment
            flipped_num = flip(num, 0)
            if flipped_num != num:
                current_segment = flipped_num
                result += 1
    
    return result

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    print(max_segments(n, k, a))