import sys

def has_palindrome_subsequence(a):
    n = len(a)
    # Create a dictionary to store the indices of each element
    index_map = {}
    for i in range(n):
        if a[i] not in index_map:
            index_map[a[i]] = []
        index_map[a[i]].append(i)
    
    # Check for palindromic subsequences of length at least 3
    for indices in index_map.values():
        if len(indices) >= 2:
            # Check if there exists another element between any two identical elements
            for i in range(len(indices) - 1):
                left = indices[i]
                right = indices[i + 1]
                # Find the smallest index greater than left and largest index less than right
                min_index = max(index for index in indices if index > left)
                max_index = min(index for index in indices if index < right)
                if min_index < max_index:
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