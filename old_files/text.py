import json

starter_messages = [
    {
        "role": "system",
        "content": "You are generating voiceover text for youtube shorts, "
        + "the voiceover must be 20-35 seconds. It must also be sensational in nature",
    }
]


def generate_model_response(client, category, topic, model="gpt-3.5-turbo", temperature=0.5):
    if category == "quote":
        prompt = f"Generate 3 interesting quotes by {topic}:\n"
        introduction = f"Did you know {topic} once said: "
    elif category == "fact":
        prompt = f"Generate 3 interesting trivia facts about {topic}:\n"
        introduction = f"Did you know these 3 unknown facts about {topic}? "

    new_messages = starter_messages + [{"role": "user", "content": prompt}]
    chat_completion = client.chat.completions.create(model=model, messages=new_messages, temperature=temperature)
    response = introduction + chat_completion.choices[0].message.content + " subscribe for more quotes and facts!!"
    short_info = {"thing": topic, "prompt": prompt, "response": response, "category": "fact"}

    return short_info


def generate_facts(client, things, save=True, filename="facts.json", model="gpt-3.5-turbo", temperature=0.5):
    facts = []

    for thing in things:
        fact = generate_model_response(client, "fact", thing, model=model, temperature=temperature)
        facts.append(fact)

    if save:
        with open(filename, "w") as fp:
            json.dump(facts, fp, indent=4)

    return facts


def generate_quotes(client, people, save=True, filename="quotes.json", model="gpt-3.5-turbo", temperature=0.5):
    quotes = []

    for person in people:
        quote = generate_model_response(client, "quote", person, model=model, temperature=temperature)
        quotes.append(quote)

    if save:
        with open(filename, "w") as fp:
            json.dump(quotes, fp, indent=4)

    return quotes
