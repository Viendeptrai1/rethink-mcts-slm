import sys

def find_sequence(n):
    # Start with an empty sequence
    sequence = []
    
    # We need to add '1337' enough times to get at least n subsequences
    # Each '1337' we add will contribute to the count of subsequences
    # Specifically, if we have k '1337's, we have k * (k + 1) / 2 subsequences
    # We need to find the smallest k such that k * (k + 1) / 2 >= n
    
    k = 0
    while k * (k + 1) // 2 < n:
        k += 1
    
    # Now we know we need at least k '1337's
    # Add '1337' k times to the sequence
    for _ in range(k):
        sequence.append('1337')
    
    # If we have more than n subsequences, we need to remove some
    # Each '1337' we remove will reduce the count by (k - 1)
    # We need to remove enough '1337's to get exactly n subsequences
    extra_subsequences = k * (k + 1) // 2 - n
    while extra_subsequences > 0:
        sequence.pop()
        k -= 1
        extra_subsequences = k * (k + 1) // 2 - n
    
    # Join the list into a single string and return
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