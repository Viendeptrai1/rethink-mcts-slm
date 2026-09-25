import sys

def is_substring(a, b):
    return a in b

def can_reorder(strings):
    # Sort strings by length in descending order
    strings.sort(key=len, reverse=True)
    
    # Check if we can reorder the strings
    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            if not is_substring(strings[j], strings[i]):
                return False
    return True

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    if can_reorder(strings):
        print("YES")
        for s in strings:
            print(s)
    else:
        print("NO")

if __name__ == "__main__":
    main()