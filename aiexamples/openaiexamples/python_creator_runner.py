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
      {
      "role": "system",
      "content": "You will be provided with text describing a desired python program/\
                  Your task is to generate the python code that will implement the described program.\
                  The code should be correct and complete as it will be automatically saved and executed.\
                  Return only the code, without any additional information."
      },
      user_message],
    temperature=0.7,
    max_tokens=2000,
    top_p=1
  )
  return response

os.chdir('./aiexamples/openaiexamples')
while True:
  # Get user input
  user_input = input("Enter python program to create and run: ")

  # Check if user wants to exit
  if user_input == 'exit':
    break

  # Call the helper function
  response = send_message(client, user_input)
  # Get response from AI
  actualResponse = response.choices[0].message.content
  print("Generated Code = " + actualResponse)

  # Save the code to a new file called generated_code.py
  with open('generated_code.py', 'w') as file:
    file.write(actualResponse)  # write the fixed code to the new file
    # run the generated code
  exec(open('generated_code.py').read())  # execute the generated code
  

