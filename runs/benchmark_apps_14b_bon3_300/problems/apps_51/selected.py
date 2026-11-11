import sys

def find_possible_message(t):
    n = len(t)
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            candidate = t[:i]
            repeated = candidate * (n // i)
            if repeated == t:
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