import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    students = []
    for i in range(N):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        students.append((a, b))
    
    checkpoints = []
    for j in range(M):
        c = int(data[2 + 2 * N + 2 * j])
        d = int(data[3 + 2 * N + 2 * j])
        checkpoints.append((c, d))
    
    results = []
    for student in students:
        min_distance = float('inf')
        min_index = -1
        for index, checkpoint in enumerate(checkpoints):
            distance = abs(student[0] - checkpoint[0]) + abs(student[1] - checkpoint[1])
            if distance < min_distance:
                min_distance = distance
                min_index = index + 1
        results.append(min_index)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()