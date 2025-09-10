"""
Enhanced Minimal LangChain Demo
A slightly more advanced 3-step chain with memory and sequential processing
"""
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFaceHub
from langchain_community.llms import Ollama

def main():
    # Step 1: Load environment variables and initialize components
    load_dotenv()
    
    # Initialize the language model with temperature for creativity
    llm = OpenAI(temperature=0.7)

    # Initialize Ollama as our second LLM
    llm2 = Ollama(
        model="llama3.1:latest",  # Using your locally installed llama3.1 model
        temperature=0.7,
        num_predict=100, # Similar to max_tokens
        verbose=False
    )
    
    # Step 2: Define two different prompt templates for our chain stages
    
    # First prompt template: Generate a short story about a topic
    first_prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a very short story about {topic} in 3-4 sentences."
    )
    
    # Second prompt template: Generate a moral lesson from the story
    second_prompt = PromptTemplate(
        input_variables=["story"],
        template="Based on this story:\n\n{story}\n\nWhat's a single moral lesson we can learn? Keep it to one sentence."
    )
    
    # Create chains for each step
    story_chain = LLMChain(llm=llm, prompt=first_prompt)
    moral_chain = LLMChain(llm=llm2, prompt=second_prompt)
    
    # Step 3: Combine the chains in sequence
    overall_chain = SimpleSequentialChain(
        chains=[story_chain, moral_chain],
        verbose=True
    )
    
    # Get user input
    user_topic = input("\nEnter a topic for a short story: ")
    
    # Process through the sequential chain
    result = overall_chain.run(user_topic)
    
    # Display final result
    print("\n" + "="*50)
    print("Moral of the Story:")
    print("="*50)
    print(result.strip())
    print("="*50)

if __name__ == "__main__":
    print("="*50)
    print("Enhanced Minimal LangChain Demo")
    print("="*50)
    main()
