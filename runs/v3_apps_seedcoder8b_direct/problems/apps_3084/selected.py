def find_times_to_set_clock(original_time, current_time):
    def increment_digit(digit):
        return '0' if digit == '9' else str(int(digit) + 1)

    def decrement_digit(digit):
        return '9' if digit == '0' else str(int(digit) - 1)

    def generate_possible_times(time):
        h1, h2, m1, m2 = time
        possible_times = set()

        for i in range(4):
            for j in range(2):
                if i == 0:
                    new_h1 = increment_digit(h1)
                    if int(new_h1 + h2) < 24:
                        possible_times.add(new_h1 + h2 + m1 + m2)
                if i == 1:
                    new_h2 = increment_digit(h2)
                    if int(h1 + new_h2) < 24:
                        possible_times.add(h1 + new_h2 + m1 + m2)
                if i == 2:
                    new_m1 = increment_digit(m1)
                    if int(new_m1 + m2) < 60:
                        possible_times.add(h1 + h2 + new_m1 + m2)
                if i == 3:
                    new_m2 = increment_digit(m2)
                    if int(m1 + new_m2) < 60:
                        possible_times.add(h1 + h2 + m1 + new_m2)

                for k in range(2):
                    if i == 0:
                        new_h1 = decrement_digit(h1)
                        if int(new_h1 + h2) < 24:
                            possible_times.add(new_h1 + h2 + m1 + m2)
                    if i == 1:
                        new_h2 = decrement_digit(h2)
                        if int(h1 + new_h2) < 24:
                            possible_times.add(h1 + new_h2 + m1 + m2)
                    if i == 2:
                        new_m1 = decrement_digit(m1)
                        if int(new_m1 + m2) < 60:
                            possible_times.add(h1 + h2 + new_m1 + m2)
                    if i == 3:
                        new_m2 = decrement_digit(m2)
                        if int(m1 + new_m2) < 60:
                            possible_times.add(h1 + h2 + m1 + new_m2)

        return possible_times

    original_time = original_time.replace(":", "")
    current_time = current_time.replace(":", "")

    possible_times = generate_possible_times(current_time)
    possible_times.add(original_time)

    sorted_times = sorted(possible_times)
    formatted_times = [time[:2] + ':' + time[2:] for time in sorted_times]

    print(len(formatted_times))
    for time in formatted_times:
        print(time)

import sys
input = sys.stdin.read
data = input().strip().split()
find_times_to_set_clock(data[0], data[1])