import sys

def can_distribute_candies(a, b, c):
    total_candies = a + b + c
    return "Yes" if total_candies % 2 == 0 else "No"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    a, b, c = int(data[0]), int(data[1]), int(data[2])
    result = can_distribute_candies(a, b, c)
    print(result)