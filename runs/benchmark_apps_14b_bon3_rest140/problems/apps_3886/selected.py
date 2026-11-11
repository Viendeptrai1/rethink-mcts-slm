import sys

def get_character(n, k):
    if n == 0:
        s = "What are you doing at the end of the world? Are you busy? Will you save us?"
        if k <= len(s):
            return s[k-1]
        else:
            return '.'
    
    # Length of f_0
    len_f0 = 69
    
    # Length of f_n
    len_fn = len_f0 * 2 + 3 + len_f0
    
    if k > len_fn:
        return '.'
    
    if k <= len_f0:
        return get_character(0, k)
    
    if k > len_f0 + 3 + len_f0:
        return get_character(0, k - len_f0 - 3 - len_f0)
    
    return '"'

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    index = 1
    results = []
    
    for _ in range(q):
        n = int(data[index])
        k = int(data[index + 1])
        index += 2
        results.append(get_character(n, k))
    
    print(''.join(results))

if __name__ == "__main__":
    main()