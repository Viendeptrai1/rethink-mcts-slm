from sys import stdin

def count_returnable_rooms(n, s):
    def dfs(i, visited, direction):
        if i in visited:
            return True
        visited.add(i)
        if s[i] == '>':
            if direction != 1:
                return False
            return dfs((i + 1) % n, visited, 1)
        elif s[i] == '<':
            if direction != -1:
                return False
            return dfs((i - 1 + n) % n, visited, -1)
        else:
            return dfs((i + 1) % n, visited, 1) or dfs((i - 1 + n) % n, visited, -1)

    return sum(dfs(i, set(), 1) for i in range(n))

def main():
    t = int(stdin.readline())
    results = []
    for _ in range(t):
        n = int(stdin.readline())
        s = stdin.readline().strip()
        results.append(count_returnable_rooms(n, s))
    for result in results:
        print(result)

if __name__ == "__main__":
    main()