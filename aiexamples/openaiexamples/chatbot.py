import os
import re
#run over all files in current directory that end with _code*.py and read their content into a string

from openai import OpenAI
client = OpenAI()

def send_message(client, user_input):
  user_message = {
    "role": "user",
    "content": user_input
  }
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      user_message],
    temperature=0.7,
    max_tokens=4000,
    top_p=1
  )
  return response

conversation = "" 
os.chdir('./aiexamples/openaiexamples')
while True:
  # Get user input
  user_input = input(">")
  conversation = conversation + user_input + "\n"

  # Check if user wants to exit
  if user_input == 'exit':
    break

  # Call the helper function
  response = send_message(client, conversation)
  # Get response from AI
  actualResponse = response.choices[0].message.content
  print(actualResponse)
  conversation = conversation + actualResponse + "\n"

  

