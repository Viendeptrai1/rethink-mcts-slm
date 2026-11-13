def split_words(txt):
    if ' ' in txt:
        return txt.split()
    elif ',' in txt:
        return txt.split(',')
    else:
        count = 0
        for char in txt:
            if char.islower():
                index = ord(char) - ord('a')
                if index % 2 == 1:
                    count += 1
        return count