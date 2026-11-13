def generate_color_code(n, P):
    from itertools import product

    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))

    def backtrack(current_code):
        if len(current_code) == 2**n:
            return current_code

        last_string = current_code[-1]
        for i in range(n):
            next_string = list(last_string)
            next_string[i] = '1' if next_string[i] == '0' else '0'
            next_string = ''.join(next_string)
            if hamming_distance(last_string, next_string) in P and next_string not in current_code:
                result = backtrack(current_code + [next_string])
                if result:
                    return result
        return None

    # Start with all zeros
    initial_string = '0' * n
    result = backtrack([initial_string])
    if result:
        return result
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
        for code in result:
            print(code)

if __name__ == "__main__":
    main()