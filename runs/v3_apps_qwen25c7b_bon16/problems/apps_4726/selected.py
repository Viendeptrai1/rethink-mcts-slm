def check_time_limit(m, n, t):
    algorithms = {
        1: lambda x: x,
        2: lambda x: 2 ** x,
        3: lambda x: x ** 4,
        4: lambda x: x ** 3,
        5: lambda x: x ** 2,
        6: lambda x: x * (x.bit_length() - 1),
        7: lambda x: x
    }
    
    operations = algorithms[t](n)
    return "AC" if operations <= m else "TLE"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    m = int(data[0])
    n = int(data[1])
    t = int(data[2])
    print(check_time_limit(m, n, t))