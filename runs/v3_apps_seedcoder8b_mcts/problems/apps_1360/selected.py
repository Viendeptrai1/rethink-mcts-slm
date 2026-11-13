def min_day_to_take_final_exam(n, exams):
    exams.sort(key=lambda x: (x[1], x[0]))
    dp = [0] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        a_i, b_i = exams[i - 1]
        dp[i] = min(dp[i - 1] + a_i, b_i)

    return dp[n]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    exams = []
    index = 1
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        exams.append((a_i, b_i))
        index += 2
    
    result = min_day_to_take_final_exam(n, exams)
    print(result)