from collections import deque
import sys

def word_ladder_with_addition(n, dictionary):
    start, end = dictionary[0], dictionary[1]
    word_set = set(dictionary)
    
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
    
    min_steps = bfs(start, end, word_set)
    best_word = '0'
    
    for word in dictionary:
        for i in range(len(word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                new_word = word[:i] + c + word[i+1:]
                if new_word not in word_set:
                    word_set.add(new_word)
                    steps = bfs(start, end, word_set)
                    word_set.remove(new_word)
                    if steps < min_steps:
                        min_steps = steps
                        best_word = new_word
                    elif steps == min_steps and new_word < best_word:
                        best_word = new_word
    
    if min_steps == float('inf'):
        return '0', -1
    return best_word, min_steps

def main():
    input = sys.stdin.read
    data = input().strip().split('\n')
    n = int(data[0])
    dictionary = data[1:n+1]
    best_word, min_steps = word_ladder_with_addition(n, dictionary)
    print(best_word)
    print(min_steps)

if __name__ == "__main__":
    main()