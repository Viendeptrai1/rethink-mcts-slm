import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    D = int(data[0])
    G = int(data[1])
    
    problems = []
    index = 2
    for i in range(D):
        p_i = int(data[index])
        c_i = int(data[index + 1])
        problems.append((p_i, c_i))
        index += 2
    
    problems.sort(key=lambda x: x[1] / x[0], reverse=True)
    
    total_score = 0
    problems_solved = 0
    
    for p_i, c_i in problems:
        if total_score >= G:
            break
        if total_score + c_i + 100 * p_i >= G:
            problems_solved += (G - total_score - c_i) // 100
            total_score = G
        else:
            problems_solved += p_i
            total_score += c_i + 100 * p_i
    
    print(problems_solved)

if __name__ == "__main__":
    main()