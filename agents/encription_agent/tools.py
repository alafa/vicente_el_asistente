from smolagents import tool

@tool
def ask_what_type_of_encryption():
    """
    Asks the user what type of encryption they want to use.
    """
    type_of_encryption = input("What type of encryption do you want to use? (A or B)")

    return type_of_encryption
    

@tool
def encrypt_type_A(message: str) -> str:
    """
    Returns a encrypted message based on the original message given.

    Args:
        message: The message to be encrypted
    """
    encrypted = (
        message.replace('a', 'o')
               .replace('s', 'z')
               .replace('u', 'o')
    )
    return encrypted

@tool
def encrypt_type_B(message: str) -> str:
    """
    Returns a encrypted message based on the original message given.

    Args:
        message: The message to be encrypted
    """
    encrypted = (
        message.replace('b', 'k')
               .replace('a', 'aa')
               .replace('u', 'ou')
    )
    return encrypted
