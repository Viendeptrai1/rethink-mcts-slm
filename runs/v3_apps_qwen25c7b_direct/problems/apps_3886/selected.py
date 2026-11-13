def get_character(n, k):
    if n == 0:
        s = "What are you doing at the end of the world? Are you busy? Will you save us?"
    else:
        s = "What are you doing while sending "
        s += '"' * n + s + '"' * n + "? Are you busy? Will you send "
        s += '"' * n + s + '"' * n + "?"
    
    if k <= len(s):
        return s[k-1]
    else:
        return '.'

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    results = []
    
    index = 1
    for _ in range(q):
        n = int(data[index])
        k = int(data[index+1])
        index += 2
        result = get_character(n, k)
        results.append(result)
    
    print(''.join(results))

if __name__ == "__main__":
    main()