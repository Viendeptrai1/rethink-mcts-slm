import sys

def is_substring(s1, s2):
    return s1 in s2

def can_reorder(strings):
    # Sort strings by length in descending order
    strings.sort(key=len, reverse=True)
    
    # Check if each string is a substring of the next one
    for i in range(len(strings) - 1):
        if not is_substring(strings[i], strings[i + 1]):
            return False, []
    
    return True, strings

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    possible, ordered_strings = can_reorder(strings)
    
    if possible:
        print("YES")
        for s in ordered_strings:
            print(s)
    else:
        print("NO")

if __name__ == "__main__":
    main()