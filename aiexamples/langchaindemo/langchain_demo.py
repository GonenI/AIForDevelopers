"""
Minimal LangChain Demo
A simple 3-step process demonstrating the core functionality of LangChain
"""
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

def main():
    # Step 1: Load environment variables and initialize components
    load_dotenv()
    
    # Initialize the language model
    llm = OpenAI(temperature=0.7)
    
    # Step 2: Define the prompt template
    template = """
    You are a helpful assistant that provides concise, informative responses.
    
    Question: {question}
    
    Answer:
    """
    
    prompt = PromptTemplate(
        input_variables=["question"],
        template=template
    )
    # Step 3: Create and execute the chain using the RunnableSequence pattern 
    # Old way (deprecated):    # chain = LLMChain(llm=llm, prompt=prompt):
    chain = prompt | llm
    
    # Get user input
    user_question = input("\nEnter your question: ")
      # Process the input through the chain
    result = chain.invoke({"question": user_question})
    
    # Display the result
    print("\n" + "="*50)
    print("Response:")
    print("="*50)
    print(result.strip())
    print("="*50)

if __name__ == "__main__":
    print("="*50)
    print("Minimal LangChain Demo")
    print("="*50)
    main()
