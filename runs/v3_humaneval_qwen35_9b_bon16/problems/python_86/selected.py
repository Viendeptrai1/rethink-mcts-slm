def anti_shuffle(s):
    words = s.split(' ')
    result_words = []
    for word in words:
        sorted_word = ''.join(sorted(word))
        result_words.append(sorted_word)
    return ' '.join(result_words)