def find_sequence_with_subsequences(n):
    # The sequence "1337" can be formed by choosing:
    # - '1' from the first position
    # - '3' from the second position
    # - '3' from the third position
    # - '7' from the fourth position
    # This means there is exactly one subsequence "1337" in any sequence of this form.
    
    # To form exactly n subsequences of "1337", we need to repeat the sequence "1337" n times.
    # This is because each repetition of "1337" is a distinct subsequence.
    
    # Construct the sequence by repeating "1337" n times.
    return "1337" * n

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    for i in range(1, t + 1):
        n = int(data[i])
        result = find_sequence_with_subsequences(n)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()