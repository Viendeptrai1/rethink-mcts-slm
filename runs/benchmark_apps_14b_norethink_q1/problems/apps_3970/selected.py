import sys

def largest_k_multiple_free_subset(n, k, a):
    a.sort()
    included = set()
    max_size = 0
    
    for num in a:
        if num not in included:
            max_size += 1
            included.add(num * k)
    
    return max_size

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    result = largest_k_multiple_free_subset(n, k, a)
    print(result)

if __name__ == "__main__":
    main()