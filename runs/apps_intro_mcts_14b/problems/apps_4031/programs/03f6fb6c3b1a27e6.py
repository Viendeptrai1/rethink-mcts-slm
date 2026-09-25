import sys
from itertools import permutations

def is_valid_order(strings):
    for i in range(1, len(strings)):
        if strings[i] not in strings[i-1]:
            return False
    return True

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    for perm in permutations(strings):
        if is_valid_order(perm):
            print("YES")
            for s in perm:
                print(s)
            return
    
    print("NO")

if __name__ == "__main__":
    main()