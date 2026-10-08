import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    students = []
    checkpoints = []
    
    index = 2
    for _ in range(N):
        a = int(data[index])
        b = int(data[index + 1])
        students.append((a, b))
        index += 2
    
    for _ in range(M):
        c = int(data[index])
        d = int(data[index + 1])
        checkpoints.append((c, d))
        index += 2
    
    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    results = []
    
    for student in students:
        min_distance = float('inf')
        nearest_checkpoint_index = -1
        for j, checkpoint in enumerate(checkpoints):
            distance = manhattan_distance(student, checkpoint)
            if distance < min_distance:
                min_distance = distance
                nearest_checkpoint_index = j + 1
        results.append(nearest_checkpoint_index)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()