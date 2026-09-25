import sys

def has_palindrome_subsequence(a):
    # Create a dictionary to count occurrences of each element
    count = {}
    for num in a:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1
    
    # Check if there is any element that appears at least twice
    for c in count.values():
        if c >= 2:
            return True
    
    return False

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
        
        if has_palindrome_subsequence(a):
            results.append("YES")
        else:
            results.append("NO")
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()