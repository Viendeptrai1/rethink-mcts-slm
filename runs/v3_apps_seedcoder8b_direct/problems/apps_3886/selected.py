def solve():
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
    
    def f(n):
        if n == 0:
            return "What are you doing at the end of the world? Are you busy? Will you save us?"
        else:
            previous = f(n - 1)
            return f'What are you doing while sending "{previous}"? Are you busy? Will you send "{previous}"?'
    
    results = []
    
    for n, k in queries:
        if n == 0:
            f_n = f(0)
        else:
            f_n = f(n)
        
        if k <= len(f_n):
            results.append(f_n[k - 1])
        else:
            results.append('.')
    
    print(''.join(results))