from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "you are a scientist"
    },
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)
print(response.choices[0].message.content)

print ('hello')

# initialize an array of numbers
''' initialize some objects in a list'''
