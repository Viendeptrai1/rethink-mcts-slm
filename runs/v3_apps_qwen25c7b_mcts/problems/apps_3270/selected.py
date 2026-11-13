from collections import deque

def find_min_steps(start_word, end_word, dictionary):
    def bfs(start, end, dict_set):
        queue = deque([(start, 1)])
        visited = set([start])
        while queue:
            current, steps = queue.popleft()
            if current == end:
                return steps
            for i in range(len(current)):
                for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    if char != current[i]:
                        next_word = current[:i] + char + current[i+1:]
                        if next_word in dict_set and next_word not in visited:
                            visited.add(next_word)
                            queue.append((next_word, steps + 1))
        return float('inf')

    min_steps = float('inf')
    best_word = None
    dict_set = set(dictionary)

    for word in dictionary:
        for i in range(len(word)):
            for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if char != word[i]:
                    next_word = word[:i] + char + word[i+1:]
                    if next_word not in dict_set:
                        dict_set.add(next_word)
                        steps = bfs(start_word, end_word, dict_set)
                        if steps < min_steps:
                            min_steps = steps
                            best_word = next_word
                        elif steps == min_steps:
                            best_word = min(best_word, next_word)
                        dict_set.remove(next_word)

    if best_word is None:
        return "0\n-1"
    else:
        return f"{best_word}\n{min_steps}"

# Example usage:
# input_data = """3
# CAT
# DOG
# COT"""
# print(find_min_steps("CAT", "DOG", ["CAT", "DOG", "COT"]))