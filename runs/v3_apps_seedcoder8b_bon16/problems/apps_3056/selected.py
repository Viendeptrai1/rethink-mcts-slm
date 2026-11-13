def calculate_walk_value(walk_set):
    def value_of_single_walk(walk):
        current_value = 1
        for step in walk:
            if step == 'L':
                current_value = 2 * current_value
            elif step == 'R':
                current_value = 2 * current_value + 1
            # If step is 'P', we stay in the same node, do nothing
        return current_value

    def generate_walks(walk_set):
        if not walk_set:
            yield ''
        else:
            for walk in generate_walks(walk_set[1:]):
                if walk_set[0] == '*':
                    for step in 'LRP':
                        yield step + walk
                else:
                    yield walk_set[0] + walk

    total_value = 0
    for walk in generate_walks(walk_set):
        total_value += value_of_single_walk(walk)
    
    return total_value

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    walk_set = input().strip()
    print(calculate_walk_value(walk_set))