import sys

def check_repeated_words():
    input_line = sys.stdin.readline().strip()
    words = input_line.split()
    seen_words = set()
    
    for word in words:
        if word in seen_words:
            print("no")
            return
        seen_words.add(word)
    
    print("yes")

check_repeated_words()