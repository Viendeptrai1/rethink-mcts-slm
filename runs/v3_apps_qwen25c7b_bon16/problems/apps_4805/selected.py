def check_repeated_words(phrase):
    words = phrase.split()
    seen_words = set()
    
    for word in words:
        if word in seen_words:
            return "no"
        seen_words.add(word)
    
    return "yes"

# Example usage:
if __name__ == "__main__":
    import sys
    input_line = sys.stdin.read().strip()
    result = check_repeated_words(input_line)
    print(result)