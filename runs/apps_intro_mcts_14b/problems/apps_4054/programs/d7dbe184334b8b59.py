import sys

def main():
    import sys
    input = sys.stdin.read().strip().split()
    numbers = list(map(int, input))
    
    # The task is to count the number of unique elements in the list
    unique_numbers = set(numbers)
    result = len(unique_numbers)
    
    print(result)

if __name__ == "__main__":
    main()