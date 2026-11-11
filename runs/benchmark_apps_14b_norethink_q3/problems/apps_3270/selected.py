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
    
    return float('inf')

def find_best_word_to_add(dictionary):
    start = dictionary[0]
    end = dictionary[1]
    original_length = bfs(start, end, dictionary)
    
    best_word = "0"
    min_length = original_length
    
    for i in range(2, len(dictionary)):
        temp_dict = dictionary[:i] + dictionary[i+1:]
        new_length = bfs(start, end, temp_dict)
        
        if new_length < min_length or (new_length == min_length and dictionary[i] < best_word):
            best_word = dictionary[i]
            min_length = new_length
    
    if min_length == original_length:
        return "0", -1
    elif min_length == float('inf'):
        return "0", -1
    else:
        return best_word, min_length

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    dictionary = data[1:n+1]
    
    best_word, min_length = find_best_word_to_add(dictionary)
    print(best_word)
    print(min_length)

if __name__ == "__main__":
    main()