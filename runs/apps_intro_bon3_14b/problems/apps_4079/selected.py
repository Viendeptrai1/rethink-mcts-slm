import sys

def is_diverse(s):
    # Convert the string to a list of positions in the alphabet
    positions = [ord(c) - ord('a') for c in s]
    # Check if the positions form a contiguous segment
    return len(set(positions)) == len(s) and max(positions) - min(positions) + 1 == len(s)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    results = []
    
    for i in range(1, n + 1):
        s = data[i]
        if is_diverse(s):
            results.append("Yes")
        else:
            results.append("No")
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()