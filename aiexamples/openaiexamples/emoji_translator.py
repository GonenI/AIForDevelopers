from openai import OpenAI

# Send user role message
def send_message(client, user_input):
  user_message = {
    "role": "user",
    "content": user_input
  }
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
      "role": "system",
      "content": "You will be provided with text, and your task is to translate it into emojis. Do not use any regular text. Do your best with emojis only."
      },
      user_message],
    temperature=0.7,
    max_tokens=64,
    top_p=1
  )
  return response

client = OpenAI()

# Loop for user role messages
while True:
  # Get user input
  user_input = input("Enter a text to translate: ")

  # Check if user wants to exit
  if user_input == 'exit':
    break

  # Call the helper function
  response = send_message(client, user_input)
  # Get response from AI
  actualResponse = response.choices[0].message.content
  print(actualResponse)