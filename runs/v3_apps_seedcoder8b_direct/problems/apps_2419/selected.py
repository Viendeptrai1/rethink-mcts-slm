def min_operations_to_equal(a, b):
    if a == b:
        return 0
    diff = abs(a - b)
    operations = 0
    increment = 1
    while diff > 0:
        if diff >= increment:
            diff -= increment
            operations += 1
        increment += 1
    return operations

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