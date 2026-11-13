import re

class Solution:
    def file_name_check(self, file_name):
        pattern = r'^[a-zA-Z][^\d]*\d{0,3}[^\d]*\.(txt|exe|dll)$'
        return 'Yes' if re.match(pattern, file_name) else 'No'

# Example usage:
solution = Solution()
print(solution.file_name_check("example.txt"))  # Output: 'Yes'
print(solution.file_name_check("1example.dll"))  # Output: 'No'