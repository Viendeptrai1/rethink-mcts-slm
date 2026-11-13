from collections import deque, defaultdict
import sys

def word_ladder(dictionary):
    start, end = dictionary[0], dictionary[1]
    word_set = set(dictionary)
    if start == end:
        return "0", "0"

    def get_neighbors(word):
        for i in range(len(word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                new_word = word[:i] + c + word[i+1:]
                if new_word in word_set:
                    yield new_word

    def bfs():
        queue = deque([(start, [])])
        visited = set([start])
        while queue:
            word, path = queue.popleft()
            if word == end:
                return len(path)
            for neighbor in get_neighbors(word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return float('inf')

    original_steps = bfs()
    
    best_word = "0"
    min_steps = original_steps

    for word in word_set:
        for i in range(len(word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                new_word = word[:i] + c + word[i+1:]
                if new_word not in word_set:
                    word_set.add(new_word)
                    steps = bfs()
                    if steps < min_steps or (steps == min_steps and new_word < best_word):
                        best_word = new_word
                        min_steps = steps
                    word_set.remove(new_word)

    if min_steps == original_steps:
        return "0", "-1"
    return best_word, str(min_steps)

# Read input
n = int(input())
dictionary = [input().strip() for _ in range(n)]

# Solve and print output
word_to_add, min_steps = word_ladder(dictionary)
print(word_to_add)
print(min_steps)