# application/usecases/password_usecase.py

import hashlib
import base64
from typing import Dict

class PasswordUseCase:
    def __init__(self):
        # Constructor does not need password_length anymore
        pass

    def process_strings(self, base_string: str, key_string: str) -> Dict[str, str]:
        """
        Process the base and key strings by hashing, encoding, and modifying as specified.

        Parameters:
        - base_string (str): Input string to transform to uppercase and encode.
        - key_string (str): Input string to transform to lowercase and encode.

        Returns:
        - Dict[str, str]: A dictionary containing modified Base64 representations of both strings.
        """

        # Convert and hash both strings
        base_string_upper = base_string.upper()
        key_string_lower = key_string.lower()

        # Hash the strings using SHA3-512
        hashed_base = hashlib.sha3_512(base_string_upper.encode('utf-8')).digest()
        hashed_key = hashlib.sha3_512(key_string_lower.encode('utf-8')).digest()

        # Convert hashes to Base64 and apply transformations
        base64_base = base64.b64encode(hashed_base).decode('utf-8')[::-1]  # Reversed Base64
        base64_key = ''.join([char.swapcase() for char in base64.b64encode(hashed_key).decode('utf-8')])  # Swap case

        return {"base64_base": base64_base, "base64_key": base64_key}

    def generate_password(self, base_string: str, key_string: str, password_length: int) -> str:
 
        """
        Generate a password based on two input strings and a specified length. 
        The password is built by combining characters from the processed input strings 
        and applying a set of rules to ensure specific character types are included.

        Parameters:
        - base_string (str): The base string used for password generation. 
        - key_string (str): The key string used for password generation.
        - password_length (int): The desired length of the password, 
        which will be adjusted if outside the bounds [10, 100].

        Returns:
        - str: The generated password, truncated to the desired length.
        """

        # Ensure password length is within [10, 100] bounds
        password_length = max(10, min(password_length, 100))

        # Process input strings
        strings = self.process_strings(base_string, key_string)

        base64_base = strings["base64_base"][2:]  # Skip the first 2 chars, then take every other char (odd indices)
        base64_key  = strings["base64_key"][:-2] # Skip the last 2 chars, then take every other char starting from the second (even indices)
        
        # Alternate combining string
        combined_string = ''.join(a + b for a, b in zip(base64_base, base64_key))

        # Identify required character positions in combined string
        first_non_alnum, first_lowercase, first_digit, first_uppercase = None, None, None, None

        for i, char in enumerate(combined_string):
            if not char.isalnum() and first_non_alnum is None:
                first_non_alnum = i
            elif char.islower() and first_lowercase is None:
                first_lowercase = i
            elif char.isdigit() and first_digit is None:
                first_digit = i
            elif char.isupper() and first_uppercase is None:
                first_uppercase = i

        # Set default values for missing characters
        if first_non_alnum is None:
            first_non_alnum = '@'
        if first_lowercase is None:
            first_lowercase = 'j'
        if first_digit is None:
            first_digit = '13'
        if first_uppercase is None:
            first_uppercase = 'N'

        # Build the final password by combining the selected characters
        result = (
            (combined_string[first_non_alnum] if isinstance(first_non_alnum, int) else first_non_alnum) +
            (combined_string[first_lowercase] if isinstance(first_lowercase, int) else first_lowercase) +
            (combined_string[first_digit] if isinstance(first_digit, int) else first_digit) +
            (combined_string[first_uppercase] if isinstance(first_uppercase, int) else first_uppercase)
        )

        # Modify combined_string based on the password_length before adding it to result
        if password_length < 14:
            # Take every 11th character
            combined_string = combined_string[::11]
        elif 15 <= password_length <= 25:
            # Take every 7th character
            combined_string = combined_string[::7]
        elif 26 <= password_length <= 35:
            # Take every 5th character
            combined_string = combined_string[::5]
        elif 36 <= password_length <= 57:
            # Take every 3rd character
            combined_string = combined_string[::3]
        else:  # password_length > 57
            # No changes to combined_string
            pass

        # Add the remaining characters starting from the third character of combined_string
        result += combined_string

        # Return the password truncated to the desired length
        return result[:password_length]