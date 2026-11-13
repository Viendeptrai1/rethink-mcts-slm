def max_significance(n, m, d, physics, informatics):
    # Sort physics and informatics cups by significance in descending order
    physics.sort(reverse=True, key=lambda x: x[0])
    informatics.sort(reverse=True, key=lambda x: x[0])

    # Create prefix sums for both subjects
    prefix_physics = [0] * (n + 1)
    prefix_informatics = [0] * (m + 1)
    width_physics = [0] * (n + 1)
    width_informatics = [0] * (m + 1)

    for i in range(1, n + 1):
        prefix_physics[i] = prefix_physics[i - 1] + physics[i - 1][0]
        width_physics[i] = width_physics[i - 1] + physics[i - 1][1]

    for j in range(1, m + 1):
        prefix_informatics[j] = prefix_informatics[j - 1] + informatics[j - 1][0]
        width_informatics[j] = width_informatics[j - 1] + informatics[j - 1][1]

    max_significance = 0

    # Iterate over all combinations of exposed Physics and Informatics cups
    for i in range(1, n + 1):
        if width_physics[i] > d:
            break
        for j in range(1, m + 1):
            if width_informatics[j] > d:
                break
            if width_physics[i] + width_informatics[j] <= d:
                current_significance = prefix_physics[i] + prefix_informatics[j]
                max_significance = max(max_significance, current_significance)

    return max_significance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    
    index = 3
    physics = []
    for _ in range(n):
        c = int(data[index])
        w = int(data[index + 1])
        physics.append((c, w))
        index += 2
    
    informatics = []
    for _ in range(m):
        c = int(data[index])
        w = int(data[index + 1])
        informatics.append((c, w))
        index += 2
    
    result = max_significance(n, m, d, physics, informatics)
    print(result)

if __name__ == "__main__":
    main()