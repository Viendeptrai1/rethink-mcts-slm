import sys

def has_palindrome_subsequence(a):
    n = len(a)
    # Create a frequency dictionary for each element in the array
    freq = {}
    for num in a:
        if num in freq:
            freq[num].append(num)
        else:
            freq[num] = [num]
    
    # Check for palindromic subsequences of length at least 3
    for key in freq:
        if len(freq[key]) >= 3:
            return "YES"
        elif len(freq[key]) == 2:
            # Check if there exists another element that can form a palindrome
            for other_key in freq:
                if other_key != key and len(freq[other_key]) >= 1:
                    return "YES"
    
    return "NO"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        a = list(map(int, data[index:index + n]))
        index += n
        result = has_palindrome_subsequence(a)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()