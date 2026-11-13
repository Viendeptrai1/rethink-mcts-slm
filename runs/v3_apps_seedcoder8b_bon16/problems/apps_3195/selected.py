import sys

def calculate_probability(Tg, Ty, Tr, observations, tq, cq):
    # Determine the cycle length
    cycle_length = Tg + Ty + Tr
    
    # Determine the start times for green, yellow, and red
    green_starts = [t for t, c in observations if c == 'green']
    yellow_starts = [t for t, c in observations if c == 'yellow']
    red_starts = [t for t, c in observations if c == 'red']
    
    # Calculate the possible start times
    possible_starts = set()
    
    for g in green_starts:
        for y in yellow_starts:
            for r in red_starts:
                if (y == g + Tg) and (r == y + Ty):
                    possible_starts.add(g)
    
    # Count how many times the lights will be cq at tq
    count_cq_at_tq = 0
    for start in possible_starts:
        relative_time = (tq - start) % cycle_length
        if relative_time < Tg and cq == 'green':
            count_cq_at_tq += 1
        elif Tg <= relative_time < Tg + Ty and cq == 'yellow':
            count_cq_at_tq += 1
        elif Tg + Ty <= relative_time < cycle_length and cq == 'red':
            count_cq_at_tq += 1
    
    # Calculate the probability
    probability = count_cq_at_tq / len(possible_starts)
    
    return probability

def main():
    input = sys.stdin.read
    data = input().split()
    
    Tg = int(data[0])
    Ty = int(data[1])
    Tr = int(data[2])
    n = int(data[3])
    
    observations = []
    index = 4
    for _ in range(n):
        t = int(data[index])
        c = data[index + 1]
        observations.append((t, c))
        index += 2
    
    tq = int(data[index])
    cq = data[index + 1]
    
    result = calculate_probability(Tg, Ty, Tr, observations, tq, cq)
    print(f"{result:.6f}")

if __name__ == "__main__":
    main()