import sys
from collections import deque

def find_min_steps(start_word, end_word, dictionary):
    if start_word == end_word:
        return 0, None
    
    def is_one_letter_diff(word1, word2):
        diff_count = 0
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                diff_count += 1
            if diff_count > 1:
                return False
        return True
    
    queue = deque([(start_word, 1)])
    visited = set([start_word])
    
    while queue:
        current_word, steps = queue.popleft()
        
        for word in dictionary:
            if word not in visited and is_one_letter_diff(current_word, word):
                if word == end_word:
                    return steps + 1, word
                queue.append((word, steps + 1))
                visited.add(word)
    
    return -1, None

def main():
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    dictionary = set(data[1:n+1])
    start_word = dictionary.pop()
    end_word = dictionary.pop()
    
    min_steps = float('inf')
    best_word = None
    
    for i in range(97, 123):  # ASCII values for 'a' to 'z'
        new_word = start_word[:i] + chr(i) + start_word[i+1:]
        if new_word not in dictionary and new_word != start_word and new_word != end_word:
            steps, added_word = find_min_steps(start_word, end_word, dictionary | {new_word})
            if steps != -1 and steps < min_steps:
                min_steps = steps
                best_word = new_word
    
    if best_word is None:
        print("0")
        print("-1")
    else:
        print(best_word)
        print(min_steps)

if __name__ == "__main__":
    main()