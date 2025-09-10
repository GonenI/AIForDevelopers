from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with some numbers that represent purchases. For each series, find the ones that are out of the ordinary, or suspicious, or different than the others in their series ."
    },
    {
      "role": "user",
      "content": "Series 1: 55.32,12.24,4445667.1,9,12\n \
                  Series 2: 34.5,12.24,100,19.4,200.1\n \
                  Series 3: 12,6,99,77,3,3,3,3,15,16,2\n \
                  Series 4: 4,7,4,7,4,9,7,4\n \
                  Series 5: 100,101,109,115,99,123\n"

    }
  ],
  temperature=0.7,
  max_tokens=125,
  top_p=1
)
print(response.choices[0].message.content)