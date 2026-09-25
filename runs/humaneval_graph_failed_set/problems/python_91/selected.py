import re

def is_bored(S):
    # Split the string into sentences using '.', '?', and '!' as delimiters
    sentences = re.split(r'[.!?]+', S)
    
    # Initialize the boredom count
    boredom_count = 0
    
    # Iterate over each sentence
    for sentence in sentences:
        # Strip leading and trailing whitespace
        stripped_sentence = sentence.strip()
        
        # Check if the sentence starts with "I"
        if stripped_sentence.startswith("I"):
            boredom_count += 1
    
    return boredom_count

# Example usage
print(is_bored("Hello world"))  # Output: 0
print(is_bored("The sky is blue. The sun is shining. I love this weather"))  # Output: 1