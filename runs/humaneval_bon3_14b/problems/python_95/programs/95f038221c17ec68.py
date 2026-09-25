def check_dict_case(d):
    if not d:
        return False
    
    all_lower = all(isinstance(k, str) and k.islower() for k in d)
    all_upper = all(isinstance(k, str) and k.isupper() for k in d)
    
    return all_lower or all_upper

# Test cases
print(check_dict_case({"a":"apple", "b":"banana"}))  # True
print(check_dict_case({"a":"apple", "A":"banana", "B":"banana"}))  # False
print(check_dict_case({"a":"apple", 8:"banana", "a":"apple"}))  # False
print(check_dict_case({"Name":"John", "Age":"36", "City":"Houston"}))  # False
print(check_dict_case({"STATE":"NC", "ZIP":"12345"}))  # True