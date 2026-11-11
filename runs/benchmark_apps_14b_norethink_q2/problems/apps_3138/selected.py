import sys

def count_matching_ranges(n, pages):
    count = 0
    for start in range(n):
        total_sum = 0
        total_product = 1
        for end in range(start, n):
            total_sum += pages[end]
            total_product *= pages[end]
            if total_sum == total_product and end > start:
                count += 1
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    pages = list(map(int, data[1:]))
    
    result = count_matching_ranges(n, pages)
    print(result)

if __name__ == "__main__":
    main()