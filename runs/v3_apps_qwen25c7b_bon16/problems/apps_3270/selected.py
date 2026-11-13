import sys
from collections import deque

def min_steps_to_ladder(dictionary, start_word, end_word):
    if start_word == end_word:
        return "0\n-1"
    
    def is_valid_word(word, current_word):
        return sum(c1 != c2 for c1, c2 in zip(word, current_word)) == 1
    
    def bfs():
        queue = deque([(start_word, 0)])
        visited = set([start_word])
        
        while queue:
            current_word, steps = queue.popleft()
            
            for i in range(len(current_word)):
                for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    new_word = current_word[:i] + char + current_word[i+1:]
                    
                    if new_word == end_word and new_word in dictionary:
                        return new_word, steps + 2
                    
                    if is_valid_word(new_word, current_word) and new_word not in visited and new_word in dictionary:
                        visited.add(new_word)
                        queue.append((new_word, steps + 1))
        
        return None, -1
    
    min_step = float('inf')
    best_word = None
    
    for word in dictionary:
        if len(word) == len(start_word):
            extended_dict = dictionary.copy()
            extended_dict.add(word)
            added_word, steps = bfs()
            
            if steps < min_step:
                min_step = steps
                best_word = added_word
                
    if best_word is None or min_step == float('inf'):
        return "0\n-1"
    
    return f"{best_word}\n{min_step}"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    dictionary = set(data[1:n+1])
    start_word = data[n+1]
    end_word = data[n+2]
    
    result = min_steps_to_ladder(dictionary, start_word, end_word)
    print(result)