import sys

def main():
    phrase = input().strip()
    words = phrase.split()
    seen_words = set()
    
    for word in words:
        if word in seen_words:
            print("no")
            return
        seen_words.add(word)
    
    print("yes")

if __name__ == "__main__":
    main()