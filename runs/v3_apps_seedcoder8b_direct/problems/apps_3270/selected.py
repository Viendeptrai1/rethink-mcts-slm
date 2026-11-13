from collections import deque, defaultdict
import sys

def word_ladder_with_addition(n, dictionary):
    def bfs(start, end, word_set):
        queue = deque([(start, 0)])
        visited = set([start])
        while queue:
            current_word, steps = queue.popleft()
            if current_word == end:
                return steps
            for i in range(len(current_word)):
                for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    next_word = current_word[:i] + c + current_word[i+1:]
                    if next_word in word_set and next_word not in visited:
                        visited.add(next_word)
                        queue.append((next_word, steps + 1))
        return float('inf')

    word_set = set(dictionary)
    start_word = dictionary[0]
    end_word = dictionary[1]

    # Check if there's already a path without adding any word
    min_steps = bfs(start_word, end_word, word_set)
    if min_steps != float('inf'):
        return "0", min_steps

    # Try adding each possible word
    best_word = "0"
    best_steps = -1

    for i in range(len(start_word)):
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            new_word = start_word[:i] + c + start_word[i+1:]
            if new_word not in word_set:
                word_set.add(new_word)
                steps = bfs(start_word, end_word, word_set)
                if steps < float('inf'):
                    if steps < best_steps or (steps == best_steps and new_word < best_word):
                        best_word = new_word
                        best_steps = steps
                word_set.remove(new_word)

    return best_word, best_steps

def main():
    input = sys.stdin.read
    data = input().strip().split('\n')
    n = int(data[0])
    dictionary = data[1:n+1]
    word_to_add, min_steps = word_ladder_with_addition(n, dictionary)
    print(word_to_add)
    print(min_steps)

if __name__ == "__main__":
    main()