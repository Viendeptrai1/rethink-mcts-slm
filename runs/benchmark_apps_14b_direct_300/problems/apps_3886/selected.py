import sys

def get_character(n, k):
    if n == 0:
        s = "What are you doing at the end of the world? Are you busy? Will you save us?"
        if k <= len(s):
            return s[k-1]
        else:
            return '.'
    
    # Length of f_0
    len_f0 = 75
    
    # Length of f_n for n >= 1
    len_fn = len_f0 + 2 * len_f0 + 3 + 2 * len(str(k))
    
    if k > len_fn:
        return '.'
    
    if k <= len_f0:
        return get_character(0, k)
    
    if k <= len_f0 + 2 * len_f0 + 3:
        if k == len_f0 + 1:
            return 'w'
        elif k == len_f0 + 2:
            return 'h'
        elif k == len_f0 + 3:
            return 'i'
        elif k == len_f0 + 4:
            return 'l'
        elif k == len_f0 + 5:
            return 'e'
        elif k == len_f0 + 6:
            return ' '
        elif k == len_f0 + 7:
            return 's'
        elif k == len_f0 + 8:
            return 'e'
        elif k == len_f0 + 9:
            return 'n'
        elif k == len_f0 + 10:
            return 'd'
        elif k == len_f0 + 11:
            return 'i'
        elif k == len_f0 + 12:
            return 'n'
        elif k == len_f0 + 13:
            return 'g'
        elif k == len_f0 + 14:
            return ' '
        elif k == len_f0 + 15:
            return '"'
        elif k == len_f0 + 16:
            return 'W'
        elif k == len_f0 + 17:
            return 'h'
        elif k == len_f0 + 18:
            return 'a'
        elif k == len_f0 + 19:
            return 't'
        elif k == len_f0 + 20:
            return ' '
        elif k == len_f0 + 21:
            return 'a'
        elif k == len_f0 + 22:
            return 'r'
        elif k == len_f0 + 23:
            return 'e'
        elif k == len_f0 + 24:
            return ' '
        elif k == len_f0 + 25:
            return 'y'
        elif k == len_f0 + 26:
            return 'o'
        elif k == len_f0 + 27:
            return 'u'
        elif k == len_f0 + 28:
            return ' '
        elif k == len_f0 + 29:
            return 'd'
        elif k == len_f0 + 30:
            return 'o'
        elif k == len_f0 + 31:
            return 'i'
        elif k == len_f0 + 32:
            return 'n'
        elif k == len_f0 + 33:
            return 'g'
        elif k == len_f0 + 34:
            return ' '
        elif k == len_f0 + 35:
            return '"'
        elif k == len_f0 + 36:
            return '?'
        elif k == len_f0 + 37:
            return ' '
        elif k == len_f0 + 38:
            return 'A'
        elif k == len_f0 + 39:
            return 'r'
        elif k == len_f0 + 40:
            return 'e'
        elif k == len_f0 + 41:
            return ' '
        elif k == len_f0 + 42:
            return 'y'
        elif k == len_f0 + 43:
            return 'o'
        elif k == len_f0 + 44:
            return 'u'
        elif k == len_f0 + 45:
            return ' '
        elif k == len_f0 + 46:
            return 'b'
        elif k == len_f0 + 47:
            return 'u'
        elif k == len_f0 + 48:
            return 's'
        elif k == len_f0 + 49:
            return 'y'
        elif k == len_f0 + 50:
            return '?'
        elif k == len_f0 + 51:
            return ' '
        elif k == len_f0 + 52:
            return 'W'
        elif k == len_f0 + 53:
            return 'i'
        elif k == len_f0 + 54:
            return 'l'
        elif k == len_f0 + 55:
            return 'l'
        elif k == len_f0 + 56:
            return ' '
        elif k == len_f0 + 57:
            return 'y'
        elif k == len_f0 + 58:
            return 'o'
        elif k == len_f0 + 59:
            return 'u'
        elif k == len_f0 + 60:
            return ' '
        elif k == len_f0 + 61:
            return 's'
        elif k == len_f0 + 62:
            return 'e'
        elif k == len_f0 + 63:
            return 'n'
        elif k == len_f0 + 64:
            return 'd'
        elif k == len_f0 + 65:
            return ' '
        elif k == len_f0 + 66:
            return '"'
        elif k == len_f0 + 67:
            return 'W'
        elif k == len_f0 + 68:
            return 'h'
        elif k == len_f0 + 69:
            return 'a'
        elif k == len_f0 + 70:
            return 't'
        elif k == len_f0 + 71:
            return ' '
        elif k == len_f0 + 72:
            return 'a'
        elif k == len_f0 + 73:
            return 'r'
        elif k == len_f0 + 74:
            return 'e'
        elif k == len_f0 + 75:
            return ' '
        elif k == len_f0 + 76:
            return 'y'
        elif k == len_f0 + 77:
            return 'o'
        elif k == len_f0 + 78:
            return 'u'
        elif k == len_f0 + 79:
            return ' '
        elif k == len_f0 + 80:
            return 'd'
        elif k == len_f0 + 81:
            return 'o'
        elif k == len_f0 + 82:
            return 'i'
        elif k == len_f0 + 83:
            return 'n'
        elif k == len_f0 + 84:
            return 'g'
        elif k == len_f0 + 85:
            return ' '
        elif k == len_f0 + 86:
            return '"'
        elif k == len_f0 + 87:
            return '?'
        elif k == len_f0 + 88:
            return '.'
    
    # Remaining part is the recursive part
    remaining_k = k - (len_f0 + 2 * len_f0 + 3)
    return get_character(n-1, remaining_k)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    q = int(data[0])
    results = []
    
    index = 1
    for _ in range(q):
        n = int(data[index])
        k = int(data[index + 1])
        index += 2
        results.append(get_character(n, k))
    
    print(''.join(results))

if __name__ == "__main__":
    main()