import math
from sys import stdin, stdout

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_lcm(time_list):
    lcm = time_list[0]
    for num in time_list[1:]:
        lcm = abs(lcm * num) // gcd(lcm, num)
    return lcm

def main():
    n = int(stdin.readline())
    time_list = [int(stdin.readline()) for _ in range(n)]
    lcm = find_lcm(time_list)
    stdout.write(str(lcm) + '\n')

if __name__ == "__main__":
    main()