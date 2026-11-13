def answer_queries(q, queries):
    def f(n):
        if n == 0:
            return "What are you doing at the end of the world? Are you busy? Will you save us?"
        else:
            prev = f(n - 1)
            return f"What are you doing while sending \"{prev}\"? Are you busy? Will you send \"{prev}\"?"

    results = []
    for n, k in queries:
        try:
            result = f(n)
            if k <= len(result):
                results.append(result[k - 1])
            else:
                results.append('.')
        except RecursionError:
            results.append('.')

    return ''.join(results)

if __name__ == "__main__":
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
    
    result = answer_queries(q, queries)
    print(result)