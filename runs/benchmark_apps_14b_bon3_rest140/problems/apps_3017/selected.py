import sys

def count_numbers_with_power_of_2(n, e):
    power_of_2 = str(2 ** e)
    count = 0
    
    for k in range(n + 1):
        if str(k).find(power_of_2) != -1:
            count += 1
    
    return count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    e = int(data[1])
    result = count_numbers_with_power_of_2(n, e)
    print(result)