import sys
from collections import deque

def add_word_to_minimize_steps(dictionary):
    def is_one_letter_different(word1, word2):
        return sum(c1 != c2 for c1, c2 in zip(word1, word2)) == 1

    def bfs(start, end, dictionary):
        queue = deque([(start, 0)])
        visited = set([start])
        while queue:
            current, steps = queue.popleft()
            if current == end:
                return steps
            for word in dictionary:
                if word not in visited and is_one_letter_different(current, word):
                    visited.add(word)
                    queue.append((word, steps + 1))
        return float('inf')

    start_word = dictionary[0]
    end_word = dictionary[1]
    original_length = bfs(start_word, end_word, dictionary[1:])
    
    if original_length < float('inf'):
        return "0", original_length

    min_steps = float('inf')
    best_word = ""

    for i in range(1, len(start_word) + 1):
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            for j in range(len(dictionary)):
                new_word = dictionary[j][:i] + letter + dictionary[j][i+1:]
                if new_word not in dictionary:
                    temp_dict = dictionary[:]
                    temp_dict.insert(j, new_word)
                    new_length = bfs(start_word, end_word, temp_dict[1:])
                    if new_length < min_steps or (new_length == min_steps and new_word < best_word):
                        min_steps = new_length
                        best_word = new_word

    if min_steps == float('inf'):
        return "0", -1
    else:
        return best_word, min_steps

if __name__ == "__main__":
    n = int(sys.stdin.readline().strip())
    dictionary = [sys.stdin.readline().strip() for _ in range(n)]
    result_word, result_steps = add_word_to_minimize_steps(dictionary)
    print(result_word)
    print(result_steps)