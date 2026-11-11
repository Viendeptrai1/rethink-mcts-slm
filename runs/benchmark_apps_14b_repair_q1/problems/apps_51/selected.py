import sys

def find_possible_message(t):
    n = len(t)
    for i in range(1, n // 2 + 1):
        if t[:i] == t[n - i:]:
            candidate = t[:n - i]
            if candidate * 2 == t[:n - i] + t[n - i:2 * n - 2 * i]:
                return "YES", candidate
    return "NO", ""

def main():
    import sys
    t = sys.stdin.read().strip()
    result, message = find_possible_message(t)
    print(result)
    if result == "YES":
        print(message)

if __name__ == "__main__":
    main()