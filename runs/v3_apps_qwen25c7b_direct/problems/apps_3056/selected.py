def calculate_walk_value(walk_set):
    def evaluate_walk(walk):
        current_node = 1
        for move in walk:
            if move == 'L':
                current_node *= 2
            elif move == 'R':
                current_node = current_node * 2 + 1
        return current_node

    def generate_walks(pattern):
        if not pattern:
            yield ''
        else:
            for walk in generate_walks(pattern[1:]):
                if pattern[0] == '*':
                    yield 'L' + walk
                    yield 'R' + walk
                    yield 'P' + walk
                else:
                    yield pattern[0] + walk

    total_value = 0
    for walk in generate_walks(walk_set):
        total_value += evaluate_walk(walk)
    return total_value

# Example usage:
if __name__ == "__main__":
    import sys
    input_string = sys.stdin.read().strip()
    result = calculate_walk_value(input_string)
    print(result)