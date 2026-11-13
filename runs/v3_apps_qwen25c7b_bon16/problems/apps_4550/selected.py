import sys

def can_distribute_candies(a, b, c):
    total_candies = a + b + c
    if total_candies % 2 != 0:
        return "No"
    target = total_candies // 2
    if (target >= a) and (target >= b) and (target >= c):
        return "Yes"
    return "No"

if __name__ == "__main__":
    input_data = sys.stdin.read().strip()
    a, b, c = map(int, input_data.split())
    result = can_distribute_candies(a, b, c)
    print(result)