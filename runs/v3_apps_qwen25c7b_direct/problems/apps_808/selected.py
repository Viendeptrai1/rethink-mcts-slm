def simple_exponential_notation(x):
    import sys
    import io
    
    # Redirect stdin and stdout to capture input and output
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(x)
    sys.stdout = io.StringIO()
    
    # Call the main function (assuming it's defined elsewhere or in the same script)
    main()
    
    # Get the captured output
    result = sys.stdout.getvalue().strip()
    
    # Restore original stdin and stdout
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    
    return result

# Define the main function to handle the conversion
def main():
    x = float(input())
    if x == int(x):
        print(f"{int(x)}")
    else:
        a, b = "{:.50e}".format(x).split('e')
        a = float(a)
        b = int(b)
        if b == 0:
            print(f"{a}")
        elif a >= 10:
            a /= 10
            b += 1
        print(f"{a}E{b}")

# Example usage
if __name__ == "__main__":
    main()