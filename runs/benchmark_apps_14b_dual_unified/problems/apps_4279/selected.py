import sys

def find_digit_at_position(k):
    length = 0
    i = 1
    while length + i * len(str(i)) < k:
        length += i * len(str(i))
        i += 1
    k -= length
    num = 10**(i-1) + (k - 1) // i
    digit_index = (k - 1) % i
    return str(num)[digit_index]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    results = []
    for i in range(1, q + 1):
        k = int(data[i])
        results.append(find_digit_at_position(k))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()