"""
Web Search Demo
A simple demonstration of using LangChain to search the web and process results
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

def main():
    # Step 1: Load environment variables and initialize components
    load_dotenv()
    
    # Initialize the language model
    llm = ChatOpenAI(
        temperature=0,  # Lower temperature for more consistent results
        model="gpt-3.5-turbo"
    )
    
    # Step 2: Set up the search tool
    search = DuckDuckGoSearchRun()
    
    print("=" * 50)
    print("Web Search for Best Israeli Pizza Demo")
    print("=" * 50)
    print("Searching for information about the best Israeli pizzerias...")
    
    # Step 3: Perform the web search
    search_query = "The Best Pizzerias in NYC"
    search_results = search.run(search_query)
    
    # Step 4: Create a prompt to extract pizza place names
    prompt = PromptTemplate(
        input_variables=["search_results"],
        template="""
        Based on the following search results about NYC pizza restaurants, 
        extract a list of up to 10 of the best NYC pizzeria names.
        
        If the same restaurant is mentioned multiple times, only include it once.
        Format your response as a numbered list with ONLY the restaurant names.
        If the information is not related to NYC pizzerias respond with "No relevant information found."
        Search Results:
        {search_results}

        List of Best NYC Pizzerias (up to 10):
        """
    )
    
    # Step 5: Create a chain to process the results
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Step 6: Process the search results
    result = chain.run(search_results=search_results)
    
    # Step 7: Display the results
    print("\n" + "=" * 50)
    print("Best NYC Pizzerias:")
    print("=" * 50)
    print(result.strip())
    print("=" * 50)

if __name__ == "__main__":
    main()
