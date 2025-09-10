import openai

# declare client variable to use in the next section
client = openai.Client()


# Updated code to use the newer OpenAI Chat Completion A
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Answer as a friendly Texan rancher"},
        {"role": "user", "content": "Hi my name is Gonen"},
    ]
    )
print(completion.choices[0].message.content)    

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Answer as a friendly Texan rancher"},
        {"role": "user", "content": "What's my name?"},
    ]
    )
print(completion.choices[0].message.content)   
