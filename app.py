# Update for app.py

# Reset Code
RESET_CODE = "7777"

# Improved validation function

def validate_code(input_code):
    if input_code.isdigit() and len(input_code) == 4:
        return input_code == RESET_CODE
    return False
