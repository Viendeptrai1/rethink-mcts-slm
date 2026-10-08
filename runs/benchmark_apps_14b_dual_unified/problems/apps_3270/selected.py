import sys
from collections import deque

def bfs(start, end, dictionary):
    queue = deque([(start, 0)])
    visited = set([start])
    
    while queue:
        current, steps = queue.popleft()
        if current == end:
            return steps
        
        for i in range(len(current)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != current[i]:
                    new_word = current[:i] + c + current[i+1:]
                    if new_word in dictionary and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, steps + 1))
    
    return -1

def find_best_word_to_add(dictionary, start, end):
    min_steps = bfs(start, end, set(dictionary))
    best_word = '0'
    
    for word in dictionary:
        possible_words = set()
        for i in range(len(word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    possible_words.add(new_word)
        
        new_dictionary = set(dictionary) | possible_words
        new_steps = bfs(start, end, new_dictionary)
        
        if new_steps != -1 and (min_steps == -1 or new_steps < min_steps):
            min_steps = new_steps
            best_word = min(possible_words)
        elif new_steps != -1 and new_steps == min_steps:
            best_word = min(best_word, min(possible_words))
    
    if min_steps == -1:
        return '0', -1
    return best_word, min_steps

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    dictionary = data[1:n+1]
    start = dictionary[0]
    end = dictionary[1]
    
    best_word, min_steps = find_best_word_to_add(dictionary, start, end)
    print(best_word)
    print(min_steps)

if __name__ == "__main__":
    main()