import sys

def is_substring(s1, s2):
    return s1 in s2

def can_reorder(strings):
    n = len(strings)
    for i in range(n):
        for j in range(i + 1, n):
            if not is_substring(strings[i], strings[j]):
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
        print("\n".join(strings))
    else:
        print("NO")

if __name__ == "__main__":
    main()