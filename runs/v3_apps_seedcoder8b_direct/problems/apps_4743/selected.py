def translate_to_nimionese(sentence):
    hard_consonants = 'bcdfgkpt'
    nearest_consonant = {'b': 'd', 'c': 'd', 'd': 'd', 'f': 'g', 'g': 'g', 'k': 'g', 'p': 't', 't': 't'}
    ending_consonants = {'b': 'ah', 'c': 'ah', 'd': 'ah', 'g': 'oh', 'k': 'oh', 'n': 'ah', 'p': 'uh', 't': 'uh'}

    def convert_word(word):
        if not word:
            return word

        first_letter = word[0].lower()
        if first_letter in hard_consonants:
            word = nearest_consonant[first_letter] + word[1:]

        word = word.replace('each', 'dach')
        word = word.replace('hip-po', 'gip-go')

        for i in range(1, len(word)):
            if word[i] in hard_consonants and word[i-1] in hard_consonants:
                word = word[:i] + first_letter + word[i+1:]

        last_hard_consonant = None
        for char in reversed(word):
            if char in hard_consonants:
                last_hard_consonant = char
                break

        if last_hard_consonant:
            word += ending_consonants[last_hard_consonant]
        else:
            word += 'ah'

        if word[0].isupper():
            word = word.capitalize()

        return word

    words = sentence.split()
    nimionese_words = [convert_word(word.replace('-', '')) for word in words]
    return ' '.join(nimionese_words)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(translate_to_nimionese(input))