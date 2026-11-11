import sys

def find_digit_at_position(k):
    length = 0
    block = 0
    while length < k:
        block += 1
        length += block * 9 * (10 ** (block - 1))
    
    length -= block * 9 * (10 ** (block - 1))
    k -= length
    
    num = 10 ** (block - 1) + (k - 1) // block
    digit_index = (k - 1) % block
    
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
    
    print('\n'.join(results))

if __name__ == "__main__":
    main()