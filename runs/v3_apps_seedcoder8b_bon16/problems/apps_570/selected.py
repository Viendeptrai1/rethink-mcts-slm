def determine_first_to_fail(a, b):
    turn = 0  # 0 for Vladik, 1 for Valera
    vladik_candies = a
    valera_candies = b
    
    while True:
        if turn == 0:  # Vladik's turn
            if vladik_candies >= valera_candies + 1:
                vladik_candies -= 1
                valera_candies += 2
            else:
                print("Vladik")
                return
        else:  # Valera's turn
            if valera_candies >= vladik_candies + 1:
                valera_candies -= 1
                vladik_candies += 3
            else:
                print("Valera")
                return
        turn = 1 - turn  # Switch turns

import sys

def main():
    input_data = sys.stdin.read().strip()
    a, b = map(int, input_data.split())
    determine_first_to_fail(a, b)

if __name__ == "__main__":
    main()