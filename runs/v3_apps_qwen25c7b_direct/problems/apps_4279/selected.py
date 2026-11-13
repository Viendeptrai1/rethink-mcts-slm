def get_digit_at_position(k):
    n = 1
    while True:
        length = n * (n + 1) // 2
        if k <= length:
            return int(str(n)[(k - 1) % n])
        k -= length
        n += 1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    queries = list(map(int, data[1:]))
    
    results = [get_digit_at_position(k) for k in queries]
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()