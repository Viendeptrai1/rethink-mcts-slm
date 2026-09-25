import sys

def remove_duplicates(arr):
    seen = set()
    result = []
    for num in reversed(arr):
        if num not in seen:
            seen.add(num)
            result.append(num)
    return list(reversed(result))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    arr = list(map(int, data[1:]))
    
    unique_elements = remove_duplicates(arr)
    x = len(unique_elements)
    
    print(x)
    print(' '.join(map(str, unique_elements)))

if __name__ == "__main__":
    main()