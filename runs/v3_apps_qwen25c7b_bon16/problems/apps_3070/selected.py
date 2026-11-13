from sys import stdin, stdout

def earliest_train_journey(N, M, trains):
    max_delay = 0
    for x, s, t, l in trains:
        if s + l > t + l:
            return 'impossible'
        max_delay = max(max_delay, t + l)
    
    for x, s, t, l in trains:
        if max_delay >= s:
            return s
    
    return 'impossible'

if __name__ == "__main__":
    input = stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    trains = []
    index = 2
    for _ in range(M):
        X = int(data[index])
        S = int(data[index + 1])
        T = int(data[index + 2])
        L = int(data[index + 3])
        trains.append((X, S, T, L))
        index += 4
    
    result = earliest_train_journey(N, M, trains)
    stdout.write(f"{result}\n")