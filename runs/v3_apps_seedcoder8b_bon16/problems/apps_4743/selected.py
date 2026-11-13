def nimionese_translation(sentence):
    hard_consonants = {'b', 'c', 'd', 'g', 'k', 'n', 'p', 't'}
    nearest_hard_consonants = {'b': 'd', 'c': 'g', 'd': 'd', 'g': 'g', 'k': 'n', 'n': 'n', 'p': 't', 't': 't'}
    vowel_consonants = {'a', 'e', 'i', 'o', 'u'}

    def replace_first_letter(word):
        first_letter = word[0]
        if first_letter in hard_consonants:
            return nearest_hard_consonants[first_letter] + word[1:]
        return word

    def replace_hard_consonants(word):
        start_letter = word[0]
        new_word = start_letter
        for i in range(1, len(word)):
            if word[i] in hard_consonants:
                if word[i] == start_letter:
                    new_word += word[i]
                else:
                    new_word += start_letter
            else:
                new_word += word[i]
        return new_word

    def add_closing_consonant(word):
        last_letter = word[-1]
        if last_letter in hard_consonants:
            if last_letter == 'b':
                word += 'ah'
            elif last_letter == 'c':
                word += 'ah'
            elif last_letter == 'd':
                word += 'ah'
            elif last_letter == 'g':
                word += 'oh'
            elif last_letter == 'k':
                word += 'uh'
            elif last_letter == 'n':
                word += 'uh'
            elif last_letter == 'p':
                word += 'uh'
            elif last_letter == 't':
                word += 'uh'
        else:
            word += 'ah'
        return word

    def convert_word(word):
        word = word.replace('each', 'dach')
        word = word.replace('hip-po', 'gip-go')
        word = word.replace('dog', 'dogah')
        word = word.replace('hip', 'gipoh')

        word = replace_first_letter(word)
        word = replace_hard_consonants(word)
        word = add_closing_consonant(word)

        return word

    words = sentence.split()
    nimion_words = [convert_word(word) for word in words]

    return ' '.join(nimion_words)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(nimionese_translation(input))