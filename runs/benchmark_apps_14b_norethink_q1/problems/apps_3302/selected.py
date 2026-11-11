import sys

def generate_gray_code(n):
    if n == 1:
        return ['0', '1']
    else:
        prev_gray = generate_gray_code(n - 1)
        return [f'0{x}' for x in prev_gray] + [f'1{x}' for x in reversed(prev_gray)]

def is_valid_color_code(code, P):
    for i in range(len(code) - 1):
        diff = sum(1 for a, b in zip(code[i], code[i + 1]) if a != b)
        if diff not in P:
            return False
    return True

def find_color_code(n, P):
    gray_code = generate_gray_code(n)
    if is_valid_color_code(gray_code, P):
        return [''.join(x) for x in gray_code]
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