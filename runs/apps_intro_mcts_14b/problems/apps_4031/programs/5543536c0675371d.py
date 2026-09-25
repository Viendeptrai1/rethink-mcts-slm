import sys

def is_substring(a, b):
    return a in b

def can_reorder(strings):
    strings.sort(key=len)
    n = len(strings)
    
    # Try to place each string in order
    for i in range(1, n):
        placed = False
        for j in range(i):
            if is_substring(strings[i], strings[j]):
                # Move strings[i] to position j+1
                strings.insert(j + 1, strings.pop(i))
                placed = True
                break
        if not placed:
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