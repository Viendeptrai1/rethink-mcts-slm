import sys

def max_operations(N, a):
    operations = 0
    while True:
        divisible_by_2 = [i for i in range(N) if a[i] % 2 == 0]
        divisible_by_3 = [i for i in range(N) if a[i] % 3 == 0]
        
        if len(divisible_by_2) == 0 and len(divisible_by_3) == 0:
            break
        
        if len(divisible_by_2) > 0:
            a[divisible_by_2[0]] //= 2
        else:
            a[divisible_by_3[0]] *= 3
        
        operations += 1
    
    return operations

# Main code
input = sys.stdin.read
data = input().split()
N = int(data[0])
a = list(map(int, data[1:]))

result = max_operations(N, a)
print(result)