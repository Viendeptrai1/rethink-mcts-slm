import sys

def count_numbers_with_power_of_two(n, e):
    target = str(2 ** e)
    count = 0
    for i in range(n + 1):
        if target in str(i):
            count += 1
    return count

if __name__ == "__main__":
    n, e = map(int, input().strip().split())
    result = count_numbers_with_power_of_two(n, e)
    print(result)