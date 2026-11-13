def calculate_walk_value(walk_set: str) -> int:
    def evaluate_walk(walk: str) -> int:
        current_value = 1
        for move in walk:
            if move == 'L':
                current_value = 2 * current_value
            elif move == 'R':
                current_value = 2 * current_value + 1
            # 'P' means stay in the same node, so no change in current_value
        return current_value

    def count_possibilities(walk: str) -> int:
        # Count the number of '*' in the walk
        return walk.count('*')

    def generate_all_walks(walk: str) -> list:
        if '*' not in walk:
            return [walk]
        else:
            index = walk.index('*')
            prefix = walk[:index]
            suffix = walk[index + 1:]
            possibilities = ['L', 'R', 'P']
            all_walks = []
            for possibility in possibilities:
                all_walks.extend(generate_all_walks(prefix + possibility + suffix))
            return all_walks

    all_walks = generate_all_walks(walk_set)
    total_value = sum(evaluate_walk(walk) for walk in all_walks)
    return total_value

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = calculate_walk_value(input)
    print(result)