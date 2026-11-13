def max_operations(N, a):
    def can_divide_by_2(x):
        return x % 2 == 0

    def count_divisions(x):
        count = 0
        while can_divide_by_2(x):
            x //= 2
            count += 1
        return count

    # Calculate the maximum number of divisions for each element
    max_divisions = [count_divisions(x) for x in a]

    # The maximum number of operations is the sum of the maximum divisions
    return sum(max_divisions)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    result = max_operations(N, a)
    print(result)