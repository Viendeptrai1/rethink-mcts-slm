import sys
from collections import deque

def bfs(start, end, dictionary):
    queue = deque([(start, 0)])
    visited = set([start])
    
    while queue:
        current, steps = queue.popleft()
        
        if current == end:
            return steps
        
        for word in dictionary:
            if word not in visited and sum(c != d for c, d in zip(current, word)) == 1:
                visited.add(word)
                queue.append((word, steps + 1))
    
    return -1

def find_best_word_to_add(dictionary, start, end):
    min_steps = bfs(start, end, dictionary)
    best_word = "Z" * len(start)  # Initialize with a word that comes last alphabetically
    
    for i in range(len(start)):
        for j in range(26):
            new_char = chr(ord('A') + j)
            new_word = start[:i] + new_char + start[i+1:]
            
            if new_word not in dictionary:
                new_dict = dictionary + [new_word]
                steps = bfs(start, end, new_dict)
                
                if steps != -1 and (steps < min_steps or (steps == min_steps and new_word < best_word)):
                    min_steps = steps
                    best_word = new_word
    
    if min_steps == bfs(start, end, dictionary):
        return "0", min_steps
    elif min_steps == -1:
        return "0", -1
    else:
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