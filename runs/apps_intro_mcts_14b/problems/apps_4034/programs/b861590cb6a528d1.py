import sys

def can_sort_by_coloring(s):
    n = len(s)
    # Create a sorted version of the string
    sorted_s = sorted(s)
    
    # Try to create a valid coloring
    coloring = []
    for i in range(n):
        if s[i] == sorted_s[i]:
            coloring.append('0')
        else:
            coloring.append('1')
    
    # Check if the coloring allows sorting
    for i in range(1, n):
        if coloring[i] == coloring[i-1] and s[i] < s[i-1]:
            return "NO"
    
    return "YES", "".join(coloring)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = can_sort_by_coloring(s)
    if result == "NO":
        print("NO")
    else:
        print("YES")
        print(result[1])

if __name__ == "__main__":
    main()