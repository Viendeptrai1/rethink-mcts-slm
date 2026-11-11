import sys

def find_sequence(n):
    # Start with an empty sequence
    sequence = []
    
    # We need to add '1337' enough times to get at least n subsequences
    # Each '1337' we add will contribute to the count of subsequences
    # Specifically, if we have k '1337's, the number of subsequences is 2^k - 1
    # We need to find the smallest k such that 2^k - 1 >= n
    k = 0
    while (1 << k) - 1 < n:
        k += 1
    
    # Now we know we need k '1337's
    for _ in range(k):
        sequence.append('1337')
    
    # If we have more than n subsequences, we need to trim some
    # The number of subsequences is 2^k - 1, so we need to remove (2^k - 1 - n) subsequences
    # We can do this by removing some '1's or '3's
    # Since we want the sequence to be as short as possible, we should remove '1's first
    # Each '1' we remove will reduce the number of subsequences by 2^(k-1)
    # So we need to remove (2^k - 1 - n) / 2^(k-1) '1's
    num_ones_to_remove = ((1 << k) - 1 - n) // (1 << (k-1))
    
    # Remove the '1's
    for i in range(num_ones_to_remove):
        sequence[i] = '337'
    
    # Join the sequence into a single string
    return ''.join(sequence)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        n = int(data[index])
        index += 1
        results.append(find_sequence(n))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()