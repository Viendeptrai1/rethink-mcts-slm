from typing import List

def below_zero(operations: List[int]) -> bool:
    current_balance = 0
    for operation in operations:
        current_balance += operation
        if current_balance < 0:
            return True
    return False