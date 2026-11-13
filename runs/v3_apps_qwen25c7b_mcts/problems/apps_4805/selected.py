def check_repeated_words():
    words = input().split()
    seen = set()
    for word in words:
        if word in seen:
            print("no")
            return
        seen.add(word)
    print("yes")

check_repeated_words()