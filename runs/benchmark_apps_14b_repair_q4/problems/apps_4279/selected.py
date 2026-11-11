def find_digit_at_position(k):
    # Step 1: Find the block number
    length = 0
    block = 0
    while length < k:
        block += 1
        length += block * len(str(block))
    
    # Step 2: Find the exact number within the block
    length -= block * len(str(block))
    k -= length
    number = int(''.join(str(i) for i in range(1, block + 1)))
    number_str = str(number)
    
    # Step 3: Extract the digit
    return number_str[k - 1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    results = []
    index = 1
    
    for _ in range(q):
        k = int(data[index])
        results.append(find_digit_at_position(k))
        index += 1
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()