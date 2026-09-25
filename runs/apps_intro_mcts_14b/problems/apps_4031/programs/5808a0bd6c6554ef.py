import sys

def is_substring(a, b):
    return a in b

def can_reorder(strings):
    n = len(strings)
    order = []
    
    while strings:
        found = False
        for i in range(len(strings)):
            if all(is_substring(s, strings[i]) for s in order):
                order.append(strings.pop(i))
                found = True
                break
        if not found:
            return "NO"
    
    return "YES", order

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    result = can_reorder(strings)
    if result == "NO":
        print("NO")
    else:
        print("YES")
        for s in result[1]:
            print(s)

if __name__ == "__main__":
    main()