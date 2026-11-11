import sys

def generate_sequence(n):
    if n == 1:
        return "1337"
    
    # We need to construct a sequence with exactly n subsequences of "1337"
    # The sequence will be in the form of "1337" followed by a series of "3"s
    # The number of "3"s added will determine the number of subsequences
    
    # To get exactly n subsequences, we need to add n-1 "3"s after "1337"
    return "1337" + "3" * (n - 1)

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
        results.append(generate_sequence(n))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()