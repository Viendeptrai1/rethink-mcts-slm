import sys

def count_numbers_with_power_of_two(n, e):
    power_of_two = str(2 ** e)
    count = 0
    for i in range(len(power_of_two)):
        for j in range(i + 1, len(power_of_two) + 1):
            if power_of_two[i:j] in str(n):
                count += 1
    return count

if __name__ == "__main__":
    input_line = sys.stdin.read().strip()
    n, e = map(int, input_line.split())
    result = count_numbers_with_power_of_two(n, e)
    print(result)