def check_unique_words():
    words = input().split()
    seen = set()
    for word in words:
        if word in seen:
            print("no")
            return
        seen.add(word)
    print("yes")

check_unique_words()