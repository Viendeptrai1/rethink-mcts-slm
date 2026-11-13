def min_operations(a, b):
    if a == b:
        return 0
    
    diff = abs(a - b)
    operations = 0
    current_sum = 0
    
    while current_sum < diff:
        operations += 1
        current_sum += operations
    
    if current_sum == diff:
        return operations
    
    while (current_sum - diff) % 2 != 0:
        operations += 1
        current_sum += operations
    
    return operations

def main():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        print(min_operations(a, b))

if __name__ == "__main__":
    main()