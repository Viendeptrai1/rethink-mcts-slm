def calculate_probability(Tg, Ty, Tr, times):
    T = times[0][0] - min(times, key=lambda x: abs(x[0] % (Tg + Ty + Tr)))[0]
    T %= (Tg + Ty + Tr)
    
    if T < Tg:
        return 1 if times[-1][1] == 'green' else 0
    elif T < Tg + Ty:
        return 1 if times[-1][1] == 'yellow' else 0
    else:
        return 1 if times[-1][1] == 'red' else 0

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
Tg = int(data[0])
Ty = int(data[1])
Tr = int(data[2])
n = int(data[3])
times = [(int(data[i*3+4]), data[i*3+5]) for i in range(n)]
t_q = int(data[n*3+4])
c_q = data[n*3+5]

# Calculate probability
probability = calculate_probability(Tg, Ty, Tr, times)

# Print result
print(probability)