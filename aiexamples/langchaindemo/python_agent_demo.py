"""
Python Executor Agent Demo
A minimal demo showing how an agent can write and execute Python code
"""
import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from io import StringIO

# Create a simple Python execution function
def python_repl(code):
    """Execute Python code and return the output."""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        # Execute the Python code
        exec(code, globals())
        sys.stdout = old_stdout
        return redirected_output.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}"

def main():
    # Step 1: Load environment variables and initialize components
    load_dotenv()
    
    # Initialize the language model (use ChatOpenAI for better tool use)
    llm = ChatOpenAI(
        temperature=0,  # Use temperature=0 for more deterministic outputs
        model="gpt-3.5-turbo"  # You can use gpt-4 for even better results
    )
    
    # Step 2: Set up our Python execution tool
    python_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl
    )
    tools = [python_tool]
    
    # Step 3: Create the agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True  # See the agent's step-by-step thinking
    )
    
    print("=" * 50)
    print("Python Executor Agent Demo")
    print("=" * 50)
    print("This agent can write and run Python code to solve problems.")
    print("Try asking it to calculate something, generate a plot, or solve a problem.")
    print("=" * 50)
      # Step 4: Get user input and run the agent
    while True:
        user_question = input("\nEnter your question (or 'exit' to quit): ")
        
        if user_question.lower() == 'exit':
            print("\nExiting the demo. Thanks for trying it out!")
            break
        
        try:
            # Process the input through the agent
            result = agent.run(user_question)
            
            # Display the result
            print("\n" + "=" * 50)
            print("Agent Response:")
            print("=" * 50)
            print(result.strip())
            print("=" * 50)
        except KeyboardInterrupt:
            print("\n\nKeyboard interrupt detected. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("This could be due to the API key configuration or a connection issue.")
            print("Make sure your OpenAI API key is correctly set in the .env file.")

if __name__ == "__main__":
    main()
