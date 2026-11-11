import sys
import bisect

def main():
    import sys
    import bisect

    def readints():
        return list(map(int, sys.stdin.read().split()))

    data = readints()
    n = data[0]
    a = data[1:]

    # Sort the ratings and their original indices
    sorted_a = sorted((val, idx) for idx, val in enumerate(a))
    
    # Initialize the result array with zeros
    result = [0] * n
    
    # Assign the smallest possible distinct ratings
    current_rating = 0
    for val, idx in sorted_a:
        current_rating = max(current_rating + 1, val)
        result[idx] = current_rating
    
    # Print the result
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()