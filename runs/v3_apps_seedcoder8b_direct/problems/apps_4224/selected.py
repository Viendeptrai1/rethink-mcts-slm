def max_operations(N, a):
    def can_divide(x):
        return x % 2 == 0

    def can_multiply(x):
        return x % 3 == 0

    operations = 0
    while True:
        new_a = []
        for num in a:
            if can_divide(num):
                new_a.append(num // 2)
            elif can_multiply(num):
                new_a.append(num * 3)
            else:
                new_a.append(num)
        
        if new_a == a:
            break
        a = new_a
        operations += 1

    return operations

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    result = max_operations(N, a)
    print(result)