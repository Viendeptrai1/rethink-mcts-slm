from sys import stdin, stdout

def generate_color_code(n, P):
    def backtrack(code):
        if len(code) == 2**n:
            return True
        last_code = code[-1]
        for i in range(2**n):
            bin_str = format(i, f'0{n}b')
            if sum(bin_str[j] != last_code[j] for j in range(n)) in P and bin_str not in code:
                if backtrack(code + [bin_str]):
                    return True
        return False
    
    start_codes = ['0'] * n
    for i in range(2**n):
        bin_str = format(i, f'0{n}b')
        if sum(bin_str[j] != '0' for j in range(n)) in P and bin_str not in start_codes:
            if backtrack([bin_str]):
                stdout.write('\n'.join(start_codes + [bin_str]))
                return
            start_codes.append(bin_str)
    
    stdout.write('impossible')

if __name__ == "__main__":
    n, p = map(int, stdin.readline().split())
    P = list(map(int, stdin.readline().split()))
    generate_color_code(n, P)