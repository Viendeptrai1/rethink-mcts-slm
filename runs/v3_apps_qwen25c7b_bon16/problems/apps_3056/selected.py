from sys import stdin, stdout

def calculate_walk_value(walk):
    current_value = 1
    for move in walk:
        if move == 'L':
            current_value *= 2
        elif move == 'R':
            current_value = current_value * 2 + 1
    return current_value

def calculate_set_value(pattern):
    from itertools import product

    def generate_walks(pattern):
        for combination in product('LRP', repeat=pattern.count('*')):
            yield ''.join(replace_star(pattern, combination))

    def replace_star(pattern, combination):
        it = iter(combination)
        return ''.join(next(it) if char == '*' else char for char in pattern)

    return sum(calculate_walk_value(walk) for walk in generate_walks(pattern))

def main():
    pattern = stdin.read().strip()
    result = calculate_set_value(pattern)
    stdout.write(str(result) + '\n')

if __name__ == "__main__":
    main()