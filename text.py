import json

starter_messages = [
    {
        "role": "system",
        "content": "You are generating voiceover text for youtube shorts, "
        + "the voiceover must be 20-35 seconds. It must also be sensational in nature",
    }
]


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
        new_messages = starter_messages.copy()
        new_messages.append({"role": "user", "content": prompt})
        chat_completion = client.chat.completions.create(model=model, messages=new_messages, temperature=temperature)
        response = f"Did you know these 3 unknown facts about {thing}? " + chat_completion.choices[0].message.content
        fact = {"thing": thing, "prompt": prompt, "response": response}
        facts.append(fact)

    if save:
        with open(filename, "w") as fp:
            json.dump(facts, fp, indent=4)

    return facts


def generate_quotes(
    client,
    people,
    save=True,
    filename="quotes.json",
    model="gpt-3.5-turbo",
    temperature=0.5,
):
    quotes = []

    for person in people:
        prompt = f"Generate 3 interesting quotes by {person}:\n"
        new_messages = starter_messages.copy()
        new_messages.append({"role": "user", "content": prompt})
        chat_completion = client.chat.completions.create(model=model, messages=new_messages, temperature=temperature)
        response = (
            f"Did you know {person} once said: "
            + chat_completion.choices[0].message.content
            + " subscribe for more quotes and facts!!"
        )
        quote = {"thing": person, "prompt": prompt, "response": response}
        quotes.append(quote)

    if save:
        with open(filename, "w") as fp:
            json.dump(quotes, fp, indent=4)

    return quotes
