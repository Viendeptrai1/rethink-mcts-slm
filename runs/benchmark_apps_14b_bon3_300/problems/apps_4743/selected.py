import sys

def translate_to_nimionese(sentence):
    def nearest_hard_consonant(char):
        hard_consonants = 'bcdfghjklmnpqrstvwxyz'
        index = hard_consonants.index(char.lower())
        return hard_consonants[index]

    def replace_first_letter(word):
        first_char = word[0].lower()
        if first_char in 'aeiou':
            return nearest_hard_consonant(first_char) + word[1:]
        return word

    def replace_subsequent_hard_consonants(word):
        first_consonant = word[0]
        new_word = list(word)
        for i in range(1, len(new_word)):
            if new_word[i] in 'bcdfghjklmnpqrstvwxyz':
                new_word[i] = first_consonant
        return ''.join(new_word)

    def add_ending(word):
        last_consonant_index = max(word.rfind(c) for c in 'bcdfghjklmnpqrstvwxyz')
        if last_consonant_index == -1:
            return word + 'ah'
        last_consonant = word[last_consonant_index]
        if last_consonant in 'bcdfg':
            return word + 'ah'
        elif last_consonant in 'hjklm':
            return word + 'oh'
        else:
            return word + 'uh'

    def translate_word(word):
        word = word.replace('-', '')
        word = replace_first_letter(word)
        word = replace_subsequent_hard_consonants(word)
        word = add_ending(word)
        return word

    words = sentence.split()
    translated_words = [translate_word(word) for word in words]
    return ' '.join(translated_words)

if __name__ == "__main__":
    input_sentence = sys.stdin.read().strip()
    output_sentence = translate_to_nimionese(input_sentence)
    print(output_sentence)