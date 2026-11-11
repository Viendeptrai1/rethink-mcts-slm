import sys

def main():
    import sys
    import collections
    
    def readints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = readints()
    a = readints()
    b = readints()
    
    # Count the frequency of each required complexity
    required_count = collections.Counter(a)
    # Count the frequency of each prepared complexity
    prepared_count = collections.Counter(b)
    
    additional_problems = 0
    
    # Check for each required complexity how many more we need
    for complexity in required_count:
        additional_problems += max(0, required_count[complexity] - prepared_count[complexity])
    
    print(additional_problems)

if __name__ == "__main__":
    main()