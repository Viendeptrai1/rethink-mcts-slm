import sys

def find_possible_message(t):
    n = len(t)
    for i in range(1, n // 2 + 1):
        if t[:n - i] == t[i:]:
            return t[:n - i]
    return None

def main():
    import sys
    t = sys.stdin.read().strip()
    possible_message = find_possible_message(t)
    if possible_message:
        print("YES")
        print(possible_message)
    else:
        print("NO")

if __name__ == "__main__":
    main()