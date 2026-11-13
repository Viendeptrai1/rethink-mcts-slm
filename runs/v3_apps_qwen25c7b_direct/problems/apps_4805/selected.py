def check_repeated_words(phrase):
    words = phrase.split()
    seen = set()
    for word in words:
        if word in seen:
            return "no"
        seen.add(word)
    return "yes"

# Example usage:
if __name__ == "__main__":
    import sys
    input_phrase = sys.stdin.read().strip()
    result = check_repeated_words(input_phrase)
    print(result)