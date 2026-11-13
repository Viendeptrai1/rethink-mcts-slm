def min_operations_to_equal(a, b):
    diff = abs(a - b)
    n = 0
    sum_n = 0
    while sum_n < diff:
        n += 1
        sum_n += n
    if sum_n == diff:
        return n
    else:
        return n + 1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    for i in range(1, t + 1):
        a = int(data[2 * i - 1])
        b = int(data[2 * i])
        results.append(min_operations_to_equal(a, b))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()