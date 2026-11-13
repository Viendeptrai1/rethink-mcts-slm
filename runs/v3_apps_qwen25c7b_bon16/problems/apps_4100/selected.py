import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
Q = int(data[2])

scores = [K] * N
answers = list(map(int, data[3:]))

for a in answers:
    scores[a - 1] -= 1

survived = ['No'] * N
for i in range(N):
    if scores[i] > 0:
        survived[i] = 'Yes'

for s in survived:
    print(s)