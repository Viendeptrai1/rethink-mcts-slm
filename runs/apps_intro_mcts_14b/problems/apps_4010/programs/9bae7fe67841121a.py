import sys

def has_palindrome_subsequence(a):
    n = len(a)
    # Create a dictionary to store the indices of each element
    index_map = {}
    for i, x in enumerate(a):
        if x not in index_map:
            index_map[x] = []
        index_map[x].append(i)
    
    # Check for each element if it appears at least twice
    for x, indices in index_map.items():
        if len(indices) >= 2:
            # Check if there exists another identical element that can form a palindrome
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    left = indices[i]
                    right = indices[j]
                    # Check for a palindrome of length 3 or more
                    if left < right:
                        for k in range(left + 1, right):
                            if a[k] == x:
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