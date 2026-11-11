import sys

def reverse_number(n):
    return int(str(n)[::-1])

def count_occurrences(A, B):
    count = 0
    for i in range(1, B + 1):
        current = i
        while current <= B:
            if current >= A:
                count += 1
            current += reverse_number(current)
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    Q = int(data[0])
    index = 1
    results = []
    
    for _ in range(Q):
        A = int(data[index])
        B = int(data[index + 1])
        index += 2
        results.append(count_occurrences(A, B))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()