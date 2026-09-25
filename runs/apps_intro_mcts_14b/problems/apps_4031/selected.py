import sys

def is_substring(s1, s2):
    return s1 in s2

def can_reorder(strings):
    n = len(strings)
    order = []
    
    while strings:
        placed = False
        for i in range(len(strings)):
            if all(is_substring(order[j], strings[i]) for j in range(len(order))):
                order.append(strings.pop(i))
                placed = True
                break
        if not placed:
            return "NO"
    
    return "YES\n" + "\n".join(order)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    result = can_reorder(strings)
    print(result)

if __name__ == "__main__":
    main()