def solve():
    N, M = map(int, input().split())
    students = [tuple(map(int, input().split())) for _ in range(N)]
    checkpoints = [tuple(map(int, input().split())) for _ in range(M)]

    results = []
    for student in students:
        min_distance = float('inf')
        nearest_checkpoint = 0
        for i, checkpoint in enumerate(checkpoints, 1):
            distance = abs(student[0] - checkpoint[0]) + abs(student[1] - checkpoint[1])
            if distance < min_distance or (distance == min_distance and i < nearest_checkpoint):
                min_distance = distance
                nearest_checkpoint = i
        results.append(nearest_checkpoint)

    for result in results:
        print(result)

if __name__ == "__main__":
    solve()