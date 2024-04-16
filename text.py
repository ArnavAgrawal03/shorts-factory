import json


def generate_facts(
    client,
    things,
    save=True,
    filename="facts.json",
    model="gpt-3.5-turbo",
    temperature=0.5,
):

    facts = []
    for thing in things:
        prompt = f"Generate 3 interesting trivia facts about {thing}:\n"
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are generating voiceover text for youtube shorts, the voiceover must be 20-35 seconds.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )

        facts.append(
            {
                "thing": thing,
                "prompt": prompt,
                "response": f"Did you know these 3 unknown facts about {thing}? "
                + chat_completion.choices[0].message.content,
            }
        )

    if save:
        with open(filename, "w") as fp:
            json.dump(facts, fp, indent=4)

    return facts
