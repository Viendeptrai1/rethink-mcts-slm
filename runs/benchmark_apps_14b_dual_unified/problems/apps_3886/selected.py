def find_character(n, k):
    if n == 0:
        s = "What are you doing at the end of the world? Are you busy? Will you save us?"
        if k <= len(s):
            return s[k-1]
        else:
            return '.'
    
    prefix = "What are you doing while sending "
    suffix = "? Are you busy? Will you send "
    
    prefix_length = len(prefix)
    suffix_length = len(suffix)
    
    inner_string_length = len(find_character(n-1, 1)) + 2  # +2 for the quotes
    
    if k <= prefix_length:
        return find_character(0, k)
    elif k > prefix_length + inner_string_length + suffix_length:
        return find_character(0, k - prefix_length - inner_string_length - suffix_length)
    else:
        if k <= prefix_length + 1:
            return '"'
        elif k > prefix_length + inner_string_length:
            return '"'
        else:
            return find_character(n-1, k - prefix_length - 1)

q = int(input())
results = []

for _ in range(q):
    n, k = map(int, input().split())
    results.append(find_character(n, k))

print(''.join(results))