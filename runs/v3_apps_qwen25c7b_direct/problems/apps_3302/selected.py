import sys

def generate_color_code(n, p, palette):
    def backtrack(path):
        if len(path) == 2**n:
            return True
        last = path[-1]
        for i in range(2**n):
            bin_str = format(i, f'0{n}b')
            if sum(last[j] != bin_str[j] for j in range(n)) in palette and bin_str not in path:
                if backtrack(path + [bin_str]):
                    return True
        return False

    for start in range(2**n):
        bin_str = format(start, f'0{n}b')
        if backtrack([bin_str]):
            return '\n'.join(path)
    return "impossible"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    p = int(data[1])
    palette = list(map(int, data[2:]))
    result = generate_color_code(n, p, palette)
    print(result)