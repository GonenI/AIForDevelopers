# Extending the LangChain Demo

Here are some simple ways to extend this minimal demo while keeping it focused:

## 1. Add More Chain Types

- **Conversation Chain**: Add memory to maintain context across multiple interactions
  ```python
  from langchain.chains import ConversationChain
  from langchain.memory import ConversationBufferMemory
  
  memory = ConversationBufferMemory()
  conversation = ConversationChain(
      llm=llm,
      memory=memory,
      verbose=True
  )
  ```

- **Question Answering**: Create a simple QA chain over your own documents
  ```python
  from langchain.chains.question_answering import load_qa_chain
  from langchain.document_loaders import TextLoader
  from langchain.text_splitter import CharacterTextSplitter
  
  documents = TextLoader("your_document.txt").load()
  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
  docs = text_splitter.split_documents(documents)
  
  chain = load_qa_chain(llm, chain_type="stuff")
  query = "What does this document say about X?"
  chain.run(input_documents=docs, question=query)
  ```

## 2. Try Different LLM Providers

Replace OpenAI with other providers:

```python
from langchain.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="google/flan-t5-xl",
    model_kwargs={"temperature": 0.7}
)
```

## 3. Add Simple Tools

Enhance with built-in tools:

```python
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType

tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the 0.23 power?")
```

Remember: The key to effective demos is clarity and focus. Add only what helps demonstrate the concept!
