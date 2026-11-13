def generate_f(n):
    if n == 0:
        return "What are you doing at the end of the world? Are you busy? Will you save us?"
    else:
        prev_f = generate_f(n-1)
        new_f = f"What are you doing while sending \"{prev_f}\"? Are you busy? Will you send \"{prev_f}\"?"
        return new_f

def get_kth_char(n, k):
    f_n = generate_f(n)
    if k <= len(f_n):
        return f_n[k-1]
    else:
        return '.'

q = int(input())
results = []
for _ in range(q):
    n, k = map(int, input().split())
    results.append(get_kth_char(n, k))

print(''.join(results))