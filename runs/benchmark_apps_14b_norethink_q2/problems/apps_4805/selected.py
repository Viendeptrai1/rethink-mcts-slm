def check_unique_words():
    import sys
    input_line = sys.stdin.read().strip()
    words = input_line.split()
    seen_words = set()
    
    for word in words:
        if word in seen_words:
            print("no")
            return
        seen_words.add(word)
    
    print("yes")

check_unique_words()