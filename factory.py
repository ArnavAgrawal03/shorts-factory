import json


def generate_text_prompt(topic, objective, audience, style, length, key_points, call_to_action):
    prompt = f"""
    Create a script for a YouTube Short video.
    
    **Topic:** {topic}
    
    **Objective:** {objective}
    
    **Audience:** {audience}
    
    **Style/Tone:** {style}
    
    **Length:** {length} seconds
    
    **Key Points to Cover:**
    {', '.join(key_points)}
    
    **Call to Action:** {call_to_action}
    
    Ensure the script is engaging and retains viewer attention throughout the video.
    """
    return prompt


def generate_prompt_prompt():
    with open("sample_prompt.json") as f:
        example = json.load(f)


def generate_text():
    prompt = generate_text_prompt(**example)
    print(prompt)
