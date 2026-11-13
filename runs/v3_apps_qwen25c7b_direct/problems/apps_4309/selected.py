def find_earliest_ABC(N):
    while True:
        if len(set(str(N))) == 1:
            return N
        N += 1

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    result = find_earliest_ABC(N)
    print(result)