import sys
input = sys.stdin.read
data = input().split()

D = int(data[0])
G = int(data[1])

problems = []
for i in range(D):
    p = int(data[2 * i + 2])
    c = int(data[2 * i + 3])
    problems.append((c, p))

problems.sort(reverse=True)

total_score = 0
solved_problems = 0

for c, p in problems:
    if total_score >= G:
        break
    if p > 0:
        total_score += p
        solved_problems += 1
        if total_score >= G:
            break
    else:
        total_score += c
        solved_problems += 1

print(solved_problems)