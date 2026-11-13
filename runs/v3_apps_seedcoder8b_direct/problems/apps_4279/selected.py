def find_digit_in_sequence(k):
    # Initialize variables to track the current block and its length
    current_block = 1
    current_block_length = 1

    # Calculate the position in the sequence where the k-th digit is located
    while k > current_block_length:
        k -= current_block_length
        current_block += 1
        current_block_length += current_block

    # Determine the exact number and digit within that number
    number = 1
    while k > len(str(number)):
        k -= len(str(number))
        number += 1

    # Return the k-th digit of the number
    return int(str(number)[k - 1])

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    queries = map(int, data[1:q+1])
    
    results = [find_digit_in_sequence(k) for k in queries]
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()