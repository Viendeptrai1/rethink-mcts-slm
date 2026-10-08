def reverse_number(n):
    return int(str(n)[::-1])

def generate_table(limit):
    table = {}
    for i in range(1, limit + 1):
        current = i
        for j in range(1, 1000):  # Arbitrary large number to ensure we cover enough terms
            if current > limit:
                break
            if current not in table:
                table[current] = 0
            table[current] += 1
            current += reverse_number(current)
    return table

def count_occurrences(table, A, B):
    count = 0
    for num in table:
        if A <= num <= B:
            count += table[num]
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    Q = int(data[0])
    index = 1
    results = []
    
    max_limit = 0
    for _ in range(Q):
        A = int(data[index])
        B = int(data[index + 1])
        max_limit = max(max_limit, B)
        index += 2
    
    table = generate_table(max_limit)
    
    index = 1
    for _ in range(Q):
        A = int(data[index])
        B = int(data[index + 1])
        results.append(count_occurrences(table, A, B))
        index += 2
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()