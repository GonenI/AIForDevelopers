import openai

def reverse_string(input_string):
    return input_string[::-1]

client = openai.Client()

instruction = (
    'when i ask you to call reverse on [somestring] simply respond with: call-reverse,and the word they asked for. '
    'for example: if i write: call reverse on racecar then you would reply: call-reverse,racecar. '
    'for all other requests reply normally.\n'
)

# Change this question to test different behaviors
#question = 'call reverse on thequickbrownfoxjumpedoverthelazydogtwotimes'  # or e.g. 'what is 5*5+1?'
question = 'who was Michael Jackson?'

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": instruction + question
        }
    ]
)

content = response.choices[0].message.content

if content.strip().startswith('call-reverse'):
    print("Response started with 'call-reverse'")
    reversed_word = content.split(',')[1].strip()
    reversed_result = reverse_string(reversed_word)
    print(f"Original: {reversed_word}")
    print(f"Reversed: {reversed_result}")
else:
    print("Response did not start with 'call-reverse'")
    print("Response content:", content)

