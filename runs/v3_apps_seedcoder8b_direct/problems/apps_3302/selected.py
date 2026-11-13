def generate_color_code(n, P):
    from itertools import product

    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))

    def backtrack(current_code):
        if len(current_code) == 2**n:
            return current_code

        last_code = current_code[-1]
        for i in range(n):
            next_code = list(last_code)
            next_code[i] = 1 - next_code[i]
            next_code = tuple(next_code)
            if next_code not in current_code and hamming_distance(last_code, next_code) in P:
                result = backtrack(current_code + [next_code])
                if result:
                    return result
        return None

    initial_code = [tuple([0] * n)]
    result = backtrack(initial_code)
    if result:
        return [''.join(map(str, code)) for code in result]
    else:
        return "impossible"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = int(data[1])
    P = set(map(int, data[2:2 + p]))
    
    result = generate_color_code(n, P)
    if result == "impossible":
        print(result)
    else:
        for line in result:
            print(line)

if __name__ == "__main__":
    main()