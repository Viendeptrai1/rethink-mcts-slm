import sys

def min_insertions_to_break_zero_sums(n, a):
    prefix_sum = 0
    seen_sums = {0}
    insertions = 0
    
    for num in a:
        prefix_sum += num
        if prefix_sum in seen_sums:
            insertions += 1
            prefix_sum += 1  # Adjust prefix sum to avoid zero sum subsegment
        seen_sums.add(prefix_sum)
    
    return insertions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = min_insertions_to_break_zero_sums(n, a)
    print(result)

if __name__ == "__main__":
    main()