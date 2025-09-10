import ollama
#response = ollama.chat(model='qwen2.5-coder:0.5b', messages=[
response = ollama.chat(model='llama3.2:latest', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue? give a one line answer',
  },
])

print(response['message']['content'])
# now with . notation 
#print(response['message'].content






