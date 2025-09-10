"""
Document QA Demo
A simple demonstration of question answering over documents using LangChain
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

def main():
    # Step 1: Load environment variables and initialize components
    load_dotenv()
    
    # Initialize the language model
    llm = ChatOpenAI(
        temperature=0,  # Lower temperature for more factual responses
        model="gpt-3.5-turbo"
    )
    
    print("=" * 50)
    print("Document QA Demo - The Hobbit")
    print("=" * 50)
    print("Loading and processing document...")
    
    # Step 2: Load the document
    document_path = "the_hobbit_pages1to10.txt"
    loader = TextLoader(document_path)
    documents = loader.load()
    
    # Step 3: Split the document into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )
    #docs = text_splitter.split_documents(documents)
    docs = documents
    
    print(f"Document loaded and split into {len(docs)} chunks.")
    
    # Step 4: Create a QA chain
    chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
    
    # Step 5: Run questions in a loop
    while True:
        print("\n" + "=" * 50)
        print("Ask a question about The Hobbit (or type 'exit' to quit)")
        print("Example questions:")
        print("- Who is Bilbo Baggins?")
        print("- What is a hobbit?")
        print("- Describe Bilbo's home.")
        print("=" * 50)
        
        question = input("Your question: ")
        
        if question.lower() == 'exit':
            print("\nExiting the Document QA Demo. Thanks for trying it out!")
            break
        
        # Process the question
        result = chain.run(input_documents=docs, question=question)
        
        # Display the result
        print("\n" + "=" * 50)
        print("Answer:")
        print("=" * 50)
        print(result.strip())
        print("=" * 50)

if __name__ == "__main__":
    main()
