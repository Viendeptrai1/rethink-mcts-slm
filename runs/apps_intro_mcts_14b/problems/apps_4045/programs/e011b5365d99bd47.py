import sys

def can_form_substring(res, s):
    return s in res or s[::-1] in res

def construct_string(n, s, t):
    res = ""
    count_a = count_b = count_c = 0
    
    for _ in range(3 * n):
        if count_a < n and not can_form_substring(res + 'a', s) and not can_form_substring(res + 'a', t):
            res += 'a'
            count_a += 1
        elif count_b < n and not can_form_substring(res + 'b', s) and not can_form_substring(res + 'b', t):
            res += 'b'
            count_b += 1
        elif count_c < n and not can_form_substring(res + 'c', s) and not can_form_substring(res + 'c', t):
            res += 'c'
            count_c += 1
        else:
            return "NO"
    
    return "YES\n" + res

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    result = construct_string(n, s, t)
    print(result)

if __name__ == "__main__":
    main()