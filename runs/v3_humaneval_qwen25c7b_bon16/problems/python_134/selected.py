import re

class Solution:
    def check_if_last_char_is_a_letter(self, txt):
        # Use regex to find all occurrences where a letter is not followed by another letter
        matches = re.findall(r'\b[a-zA-Z]\b', txt)
        # Check if the last match is at the end of the string
        return bool(matches) and txt.endswith(matches[-1])

# Function signature for call-based execution
def check_if_last_char_is_a_letter(txt):
    sol = Solution()
    return sol.check_if_last_char_is_a_letter(txt)