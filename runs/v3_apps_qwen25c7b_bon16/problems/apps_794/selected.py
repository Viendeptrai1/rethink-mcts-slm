def can_reorder(a):
    if len(a) % 2 != 0:
        return False
    left_sum = sum(a[:len(a)//2])
    right_sum = sum(a[len(a)//2:])
    if left_sum == right_sum:
        return False
    return True

def find_reorder(a):
    n = len(a)
    left_sum = sum(a[:n//2])
    right_sum = sum(a[n//2:])
    
    if left_sum == right_sum:
        return -1
    
    return a

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = find_reorder(a)
    
    if result == -1:
        print(-1)
    else:
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()