def solve_queries(q, queries):
    def f(i):
        if i == 0:
            return "What are you doing at the end of the world? Are you busy? Will you save us?"
        return f"What are you doing while sending \"{f(i-1)}\"? Are you busy? Will you send \"{f(i-1)}\"?"

    def count_chars(i):
        if i == 0:
            return 69
        return 12 * count_chars(i-1) + 8

    results = []
    for n, k in queries:
        total_chars = count_chars(n)
        if k > total_chars:
            results.append('.')
        else:
            result = f(n)
            results.append(result[k-1])

    return ''.join(results)

if __name__ == "__main__":
    q = int(input())
    queries = [tuple(map(int, input().split())) for _ in range(q)]
    print(solve_queries(q, queries))