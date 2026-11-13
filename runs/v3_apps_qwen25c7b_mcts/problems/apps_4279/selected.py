def get_digit_at_position(k):
    block_length = 0
    current_block = 0
    
    while block_length < k:
        current_block += 1
        block_length += len(str(current_block))
    
    remaining_length = k - (block_length - len(str(current_block)))
    digit_index = remaining_length - 1
    
    return int(str(current_block)[digit_index])

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    queries = [int(data[i]) for i in range(1, q + 1)]
    
    results = [get_digit_at_position(k) for k in queries]
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()