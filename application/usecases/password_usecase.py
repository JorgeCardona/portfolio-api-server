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
        Generate a password based on processed input strings and specific rules. The password is formed by combining characters
        from the processed `base_string` and `key_string` in an alternating pattern, and ensuring the inclusion of at least
        one non-alphanumeric character, one lowercase letter, one digit, and one uppercase letter. Default characters are
        used if the required characters are not found in the combined string.

        Parameters:
        - base_string (str): Base string to be processed for transformations.
        - key_string (str): Key string to be processed for transformations.
        - password_length (int): Desired length of the password (between 10 and 100 characters).

        Returns:
        - str: Generated password, truncated to the specified length.

        Notes:
        - The password will include characters from `base_string` and `key_string` based on the following rules:
        1. First, a non-alphanumeric character (default is `@` if not found).
        2. Then, a lowercase letter (default is `j` if not found).
        3. A digit (default is `13` if not found).
        4. An uppercase letter (default is `N` if not found).
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

        print(first_non_alnum, first_lowercase, first_digit, first_uppercase)
        # Build the final password by combining the selected characters
        result = (
            (combined_string[first_non_alnum] if isinstance(first_non_alnum, int) else first_non_alnum) +
            (combined_string[first_lowercase] if isinstance(first_lowercase, int) else first_lowercase) +
            (combined_string[first_digit] if isinstance(first_digit, int) else first_digit) +
            (combined_string[first_uppercase] if isinstance(first_uppercase, int) else first_uppercase)
        )

        # Add the remaining characters starting from the third character of combined_string
        result += combined_string

        # Return the password truncated to the desired length
        return result[:password_length]