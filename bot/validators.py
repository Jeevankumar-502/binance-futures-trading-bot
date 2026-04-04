import re

def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be a dictionary.')
    # Add more validation as needed
    return True
