def get_response(text, emotion):
    
    responses = {
        "happy": [
            "That's great to hear! 😊",
            "Awesome! Keep smiling 😄",
        ],
        "sad": [
            "I'm here for you 💙",
            "Don't worry, things will get better",
        ],
        "angry": [
            "Take a deep breath 😌",
            "Try to stay calm, I'm here to help",
        ],
        "neutral": [
            "Tell me more!",
            "I'm listening 🙂",
        ]
    }

    # default fallback
    if emotion not in responses:
        return "I understand. Tell me more."

    import random
    return random.choice(responses[emotion])