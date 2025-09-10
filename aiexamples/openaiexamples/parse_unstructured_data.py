from openai import OpenAI
import csv
import os
import csv
import os

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    # {
    #   "role": "system",
    #   "content": "You will be provided with unstructured data, and your task is to parse it into CSV format."
    # },
    # {
    #   "role": "user",
    #   "content": "There are many fruits that were found on the recently discovered planet Goocrux. There are neoskizzles that grow there, which are purple and taste like candy. There are also loheckles, which are a grayish blue fruit and are very tart, a little bit like a lemon. Pounits are a bright green color and are more savory than sweet. There are also plenty of loopnovas which are a neon pink flavor and taste like cotton candy. Finally, there are fruits called glowls, which have a very sour and bitter taste which is acidic and caustic, and a pale orange tinge to them."
    # }
    {
      "role": "user",
      "content": "Parse the following sentence into a 3 column csv format with headers Fruit,Color,Taste:There are many fruits that were found on the recently discovered planet Goocrux. There are neoskizzles that grow there, which are purple and taste like candy. There are also loheckles, which are a grayish blue fruit and are very tart, a little bit like a lemon. Pounits are a bright green color and are more savory than sweet. There are also plenty of loopnovas which are a neon pink flavor and taste like cotton candy. Finally, there are fruits called glowls, which have a very sour and bitter taste which is acidic and caustic, and a pale orange tinge to them."
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)


actualresponse = response.choices[0].message.content
print(actualresponse)
# now save the actualresponse as a CSV file fruits.csv in the same directory as the sourcefile 

# open the file in the write mode
with open(os.path.join(os.path.dirname(__file__), 'fruits.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the data
    for line in actualresponse.split('\n'):
        if line.strip():
            writer.writerow(line.split(','))
    file.close()

