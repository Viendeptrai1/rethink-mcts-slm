def count_possible_passwords(N):
    return N ** 3

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    result = count_possible_passwords(N)
    print(result)