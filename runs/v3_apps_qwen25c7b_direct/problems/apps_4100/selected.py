import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
Q = int(data[2])

scores = [K] * N
answers = list(map(int, data[3:]))

for answer in answers:
    scores[answer - 1] -= 1
    for i in range(N):
        if i != answer - 1:
            scores[i] -= 1

result = ['Yes' if score > 0 else 'No' for score in scores]
print('\n'.join(result))