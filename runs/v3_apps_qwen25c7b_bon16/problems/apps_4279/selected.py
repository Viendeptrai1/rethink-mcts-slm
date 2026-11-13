def get_digit(k):
    total_length = 0
    i = 1
    
    while True:
        length = len(str(i))
        if total_length + length >= k:
            return int(str(i)[k - total_length - 1])
        total_length += length
        i += 1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    queries = list(map(int, data[1:]))
    
    results = [get_digit(k) for k in queries]
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()