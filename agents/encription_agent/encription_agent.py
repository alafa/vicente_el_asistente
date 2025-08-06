from smolagents import CodeAgent, tool
from .tools import ask_what_type_of_encryption, encrypt_type_A, encrypt_type_B
from utils.load_model import model

agent = CodeAgent(
    tools=[ask_what_type_of_encryption, encrypt_type_A, encrypt_type_B],
    model=model
)

@tool
def use_encrypt_agent(message: str, type_of_encryption: str = None) -> str:
    """
    Uses the encrypt agent to encode a message.

    Args:
        message: The message to be encrypted
        type_of_encryption: The type of encryption to use (optional)
    """

    return agent.run(f"""
    Encrypt the message '{message}' with encription {type_of_encryption if type_of_encryption else 'A or B'}.
    If yo do not know what type of encription is, ask the user.
    Use tool encript_type_A for encriptions type A or encript_type_B for encription B.
    """
    )
