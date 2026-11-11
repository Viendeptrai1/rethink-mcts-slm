import sys

def find_wcd(n, pairs):
    # Find the minimum value in any pair
    min_value = min(min(a, b) for a, b in pairs)
    
    # Iterate through potential candidates starting from 2 up to the minimum value
    for candidate in range(2, min_value + 1):
        if all(a % candidate == 0 or b % candidate == 0 for a, b in pairs):
            return candidate
    
    return -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    pairs = []
    index = 1
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        pairs.append((a, b))
        index += 2
    
    result = find_wcd(n, pairs)
    print(result)

if __name__ == "__main__":
    main()