import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    prefix_sums = set()
    current_sum = 0
    insertions = 0
    
    for i in range(n):
        current_sum += a[i]
        if current_sum in prefix_sums:
            # We need to insert a number to break the zero-sum subsegment
            insertions += 1
            current_sum += 1  # Inserting a positive number to break the zero-sum
        prefix_sums.add(current_sum)
    
    print(insertions)

if __name__ == "__main__":
    main()