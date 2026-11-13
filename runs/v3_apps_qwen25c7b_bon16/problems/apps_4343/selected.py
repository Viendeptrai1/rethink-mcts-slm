def find_median(k, s, t):
    import bisect
    
    # Function to generate the next lexicographic string
    def next_string(s):
        i = len(s) - 1
        while i >= 0 and s[i] == 'z':
            i -= 1
        if i < 0:
            return None
        s = list(s)
        s[i] = chr(ord(s[i]) + 1)
        for j in range(i + 1, len(s)):
            s[j] = 'a'
        return ''.join(s)
    
    # Generate the list of strings
    start = s
    end = t
    result_list = []
    while True:
        result_list.append(start)
        start = next_string(start)
        if start is None or start > end:
            break
    
    # Find the median
    median_index = len(result_list) // 2
    median_string = result_list[median_index]
    
    return median_string

# Example usage
if __name__ == "__main__":
    k = int(input())
    s = input()
    t = input()
    print(find_median(k, s, t))