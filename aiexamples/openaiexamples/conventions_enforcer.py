import os
import re
#run over all files in current directory that end with _code*.py and read their content into a string

from openai import OpenAI
client = OpenAI()

def get_fixed_code(codetofix) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with a piece of Python code, and your task is to \
                enforce company coding conventions: every function and variable name should be in snake_case,\
                every comment should be a python comment and should start with @@@@@@.\
                pendulum should be used instead of pytz.\
                Return only the fixed code, without any additional information."
            },
            {
                "role": "user",
                "content": codetofix
            }
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1
    )
    return response.choices[0].message.content

os.chdir('./aiexamples/openaiexamples')
for filename in os.listdir('.'):
    # check using regex if file ends with _code*.py
    if re.search(r'_code\d*\.py$', filename):
        with open(filename, 'r') as file:
            code = file.read()
            print(get_fixed_code(code))
            # save the fixed code to a new file in the format filename_fixed.py
            with open(filename.replace('.py', '_fixed.py'), 'w') as fixed_file:
                fixed_file.write(get_fixed_code(code))  # write the fixed code to the new file


