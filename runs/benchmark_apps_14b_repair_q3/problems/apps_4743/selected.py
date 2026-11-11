import sys

def translate_to_nimionese(sentence):
    def nearest_hard_consonant(c):
        hard_consonants = 'bcdfgknpt'
        distances = [abs(ord(c) - ord(hc)) for hc in hard_consonants]
        min_distance = min(distances)
        return hard_consonants[distances.index(min_distance)]
    
    def replace_first_letter(word):
        first_letter = word[0].lower()
        new_first_letter = nearest_hard_consonant(first_letter)
        return new_first_letter + word[1:]
    
    def replace_subsequent_hard_consonants(word, new_first_letter):
        hard_consonants = 'bcdfgknpt'
        result = []
        for char in word:
            if char.lower() in hard_consonants:
                result.append(new_first_letter)
            else:
                result.append(char)
        return ''.join(result)
    
    def add_ending(word):
        hard_consonants = 'bcdfgknpt'
        last_hard_consonant_index = -1
        for i, char in enumerate(word):
            if char.lower() in hard_consonants:
                last_hard_consonant_index = i
        if last_hard_consonant_index == -1:
            return word + 'ah'
        else:
            ending = 'ah' if word[last_hard_consonant_index].lower() <= 'm' else 'oh'
            return word[:last_hard_consonant_index + 1] + ending
    
    def translate_word(word):
        word = word.replace('-', '')
        word = replace_first_letter(word)
        new_first_letter = word[0]
        word = replace_subsequent_hard_consonants(word[1:], new_first_letter)
        word = add_ending(word)
        return word
    
    words = sentence.split()
    translated_words = [translate_word(word) for word in words]
    return ' '.join(translated_words)

if __name__ == "__main__":
    input_sentence = sys.stdin.read().strip()
    output_sentence = translate_to_nimionese(input_sentence)
    print(output_sentence)