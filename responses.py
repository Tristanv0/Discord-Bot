import random

def handle_response(message) -> str: 
    p_message = message.lower()

    if p_message == 'roll':
        return str(random.randint(1,6))
    