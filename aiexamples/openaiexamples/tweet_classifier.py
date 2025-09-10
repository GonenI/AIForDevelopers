from openai import OpenAI
client = OpenAI()

# Send system role message
system_message = {
  "role": "system",
  "content": "You will be provided with a tweet, and your task is to classify its sentiment as positive, neutral, or negative."
}
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[system_message],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)

# Loop for user role messages
while True:
  # Get user input
  user_input = input("Enter a tweet: ")

  # Check if user wants to exit
  if user_input == 'exit':
    break

  # Send user role message
  user_message = {
    "role": "user",
    "content": user_input
  }
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[system_message, user_message],
    temperature=0.7,
    max_tokens=64,
    top_p=1
  )

  # Get response from AI
  actualResponse = response.choices[0].message.content
  print(actualResponse)