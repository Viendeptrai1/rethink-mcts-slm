import sys
from collections import deque

def add_word_to_minimize_ladder(dictionary):
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
        return -1

    start_word = dictionary[0]
    end_word = dictionary[1]
    original_length = bfs(start_word, end_word, dictionary[1:])
    
    if original_length == -1:
        return "0", "-1"
    
    min_steps = float('inf')
    best_word = "0"
    
    for i in range(1, len(dictionary)):
        temp_dict = dictionary[:i] + dictionary[i+1:]
        new_length = bfs(start_word, end_word, temp_dict)
        if new_length != -1 and new_length < original_length:
            original_length = new_length
            best_word = dictionary[i]
        elif new_length == original_length:
            best_word = min(best_word, dictionary[i])
    
    return best_word, str(original_length)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    n = int(data[0])
    dictionary = data[1:]
    result = add_word_to_minimize_ladder(dictionary)
    print(result[0])
    print(result[1])