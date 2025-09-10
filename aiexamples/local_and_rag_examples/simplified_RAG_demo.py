import ollama

instruction = 'for the following question, if the question is about sales quarter 1 respond with "quarter1", if it is about \
        sales quarter 2 respond with "quarter2", if it is about anything else, responde with "else". do not include any \
        response output as this will be processed by code. Also, do not answer the questiion itself. Merely classify it as quarter1 or quarter2 or else. \
        Question: '

question = 'What were the Chicago sales for the second quarter?'
#question = 'How many sales were made in the quarter whose number is 1+1?'

quarter_response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': instruction + question ,
  },
])

quarter = quarter_response['message']['content'].strip()


response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': question
  }])

print(f'The classified question is: {quarter}') 
if quarter in ['quarter1', 'quarter2']:
    filename = f'sales_{quarter}.txt'
    with open(filename, 'r') as file:
        sales_data = file.read()
else:
    print('Sorry, I cant answer that question.')
    exit()

response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': f'Here are the sales data for the {quarter} quarter: {sales_data}.\
        Please answer the following question:' + question ,
  }])

print(response['message']['content'])
