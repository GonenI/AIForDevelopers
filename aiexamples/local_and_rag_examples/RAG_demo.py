import openai
from openai import OpenAI
import faiss
import os
import json
import numpy as np

# Initialize the OpenAI client
client = OpenAI()
print(f"OpenAI API Key initialized")

# Update file paths to use absolute paths
sales_data = {
    "quarter1": os.path.join(os.path.dirname(__file__), "sales_quarter1.txt"),
    "quarter2": os.path.join(os.path.dirname(__file__), "sales_quarter2.txt")
}

# Function to load sales data and generate embeddings
def prepare_vector_db():
    index = faiss.IndexFlatL2(1536)  # 1536 is the dimension of OpenAI embeddings
    metadata = []

    for quarter, filename in sales_data.items():
        with open(filename, 'r') as file:
            content = file.read()
            
            # Create a rich, descriptive text for embedding that explicitly mentions the quarter
            quarter_name = "first quarter (Q1)" if quarter == "quarter1" else "second quarter (Q2)"
            enhanced_content = f"Sales data for the {quarter_name} of the year:\n{content}"
            
            # Using the correct client-based API for embeddings
            embedding_response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=enhanced_content
            )
            embedding = embedding_response.data[0].embedding
            
            # Convert the embedding to a numpy array before adding to FAISS
            embedding_np = np.array([embedding], dtype=np.float32)
            index.add(embedding_np)
            
            # Store both the original content and the enhanced content in metadata
            metadata.append({
                "quarter": quarter,
                "content": content,
                "enhanced_content": enhanced_content
            })
            
            print(f"Embedded content for {quarter}:\n{enhanced_content}\n")

    return index, metadata

# Function to query the vector database using embeddings
def query_vector_db(index, metadata, question):
    # Create an embedding for the question
    embedding_response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=question
    )
    embedding = embedding_response.data[0].embedding
    
    # Convert the embedding to a numpy array
    embedding_np = np.array([embedding], dtype=np.float32)
    
    # Search for the closest match
    distances, indices = index.search(embedding_np, k=2)
    
    # Print debug information
    print(f"Query: {question}")
    print(f"Distances: {distances[0]}")
    for i, idx in enumerate(indices[0]):
        print(f"Match {i+1}: {metadata[idx]['quarter']} (Distance: {distances[0][i]:.4f})")
    
    # Return the closest match if it's reasonably close
    return metadata[indices[0][0]] if distances[0][0] < 1.0 else None

# Main program
def main():
    question = input("Enter your question about quarterly sales: ")
    index, metadata = prepare_vector_db()
    
    # Use the vector database to find the most relevant quarterly data
    result = query_vector_db(index, metadata, question)

    if result:
        content = f"Here are the sales data for the {result['quarter']} of the year:\n{result['content']}\n\nPlease answer the following question: {question}"
        messages = [
            {"role": "system", "content": "You are a helpful sales data assistant."},
            {"role": "user", "content": content}
        ]
        
        # Using the correct client-based API for chat completions
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print("\nAnswer based on the retrieved data:")
        print(response.choices[0].message.content)
    else:
        print("Sorry, I couldn't find relevant data to answer your question.")

if __name__ == "__main__":
    main()