import sys

def find_second_largest(n, numbers):
    numbers.sort()
    return numbers[-2]

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:n+1]))
    
    result = find_second_largest(n, numbers)
    print(result)