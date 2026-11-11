import sys

def generate_string(n):
    if n == 0:
        return "What are you doing at the end of the world? Are you busy? Will you save us?"
    else:
        prev = generate_string(n - 1)
        return f'What are you doing while sending "{prev}"? Are you busy? Will you send "{prev}"?'

def solve_queries(queries):
    results = []
    for n, k in queries:
        f_n = generate_string(n)
        if k <= len(f_n):
            results.append(f_n[k - 1])
        else:
            results.append('.')
    return ''.join(results)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    queries = []
    index = 1
    for _ in range(q):
        n = int(data[index])
        k = int(data[index + 1])
        queries.append((n, k))
        index += 2
    
    result = solve_queries(queries)
    print(result)

if __name__ == "__main__":
    main()