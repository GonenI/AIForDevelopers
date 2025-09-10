from openai import OpenAI
client = OpenAI()

# upload a training file
# created_training_file = client.files.create(
#   file=open("aiexamples/openaiexamples/marv.jsonl", "rb"),
#   purpose="fine-tune"
# )
# # create a fine tuned model 
# # may take some time - you will receive an email
# response = client.fine_tuning.jobs.create(
#   training_file=created_training_file.id, 
#   model="gpt-3.5-turbo"
# )

# model_id = response.id
# print("model id = " ,model_id)
# # you can list/Retrieve/cancel the state of a fine-tune
#client.fine_tuning.jobs.list(limit=10)
#print(client.fine_tuning.jobs.retrieve("ftjob-A9MTMHZdtPmJnZAaF34wYHcZ"))
#print ("job status = ",client.fine_tuning.jobs.retrieve("ftjob-A9MTMHZdtPmJnZAaF34wYHcZ").status)


# use the fine-tuned model
completion = client.chat.completions.create(
  # you will get the model id from job when it completes
  model="ft:gpt-3.5-turbo-0125:personal::9YW6F4Cd", 
  #model="gpt-3.5-turbo" ,
  messages=[
    {"role": "system", "content": "Answer as Marv. Remain in character and answer the following question."},
    {"role": "user", "content": "Where is the Sahara desert?"},
  ]
)
print(completion.choices[0].message)
