def check_repeats(phrase):
    words = phrase.split()
    seen = set()
    for word in words:
        if word in seen:
            return "no"
        seen.add(word)
    return "yes"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(check_repeats(input))