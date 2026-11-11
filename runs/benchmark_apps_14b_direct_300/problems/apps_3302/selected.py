def generate_gray_code(n):
    def gray_code(k):
        return k ^ (k >> 1)
    
    return [format(gray_code(i), f'0{n}b') for i in range(1 << n)]

def is_valid_color_code(code, P):
    for i in range(len(code) - 1):
        diff = sum(c1 != c2 for c1, c2 in zip(code[i], code[i + 1]))
        if diff not in P:
            return False
    return True

def find_color_code(n, P):
    gray_code = generate_gray_code(n)
    if is_valid_color_code(gray_code, P):
        return gray_code
    else:
        return None

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = int(data[1])
    P = set(map(int, data[2:2+p]))
    
    result = find_color_code(n, P)
    if result:
        for code in result:
            print(code)
    else:
        print("impossible")

if __name__ == "__main__":
    main()