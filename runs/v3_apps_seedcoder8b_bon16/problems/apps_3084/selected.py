def find_minimum_steps(original, current):
    def increment_digit(digit):
        return str((int(digit) + 1) % 10)

    def decrement_digit(digit):
        return str((int(digit) - 1) % 10)

    def generate_possible_times(time):
        h1, h2, m1, m2 = time
        possible_times = []
        for i in range(4):
            for sign in [decrement_digit, increment_digit]:
                new_time = list(time)
                new_time[i] = sign(new_time[i])
                if (i < 2 and int(''.join(new_time[:2])) < 24) or (i >= 2 and int(''.join(new_time[2:])) < 60):
                    possible_times.append(''.join(new_time))
        return possible_times

    from collections import deque

    original = original.replace(":", "")
    current = current.replace(":", "")
    
    queue = deque([(original, [original])])
    visited = set(original)

    while queue:
        time, path = queue.popleft()
        if time == current:
            print(len(path))
            for step in path:
                print(step[:2] + ":" + step[2:])
            return

        for next_time in generate_possible_times(time):
            if next_time not in visited:
                visited.add(next_time)
                queue.append((next_time, path + [next_time]))

import sys
input = sys.stdin.read
data = input().strip().split("\n")
find_minimum_steps(data[0], data[1])