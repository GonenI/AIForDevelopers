import requests
import json

def get_cat_fact():
    """
    Retrieves a random cat fact from catfact.ninja API
    Returns the fact as a string, or None if the request fails
    """
    url = "https://catfact.ninja/fact"
    
    try:
        # Make GET request to the API
        response = requests.get(url)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Return the fact
        return data.get('fact')
    
    except requests.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None

if __name__ == "__main__":
    # Get and print a cat fact
    print("Getting cat fact...")
    fact = get_cat_fact()
    if fact:
        print("Cat Fact of the Day:")
        print(fact) 