def add_message(history, role, content):
    """
    Add a message to conversation history.
    """

    history.append(
        {
            "role": role,
            "content": content
        }
    )

    return history


def get_recent_history(history, max_messages=6):
    """
    Return only the most recent messages.
    """

    return history[-max_messages:]