#!/usr/bin/env python3
import sys
import json
import random

def shuffle_string(text):
    # Convert string to list of characters
    chars = list(text)
    # Shuffle the list
    random.shuffle(chars)
    # Join back into string
    return ''.join(chars)

def main():
    while True:
        try:
            # Read input from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            # Parse the JSON input
            data = json.loads(line)
            
            # Get the text to shuffle
            text = data.get('text', '')
            
            # Process the text
            result = shuffle_string(text)
            
            # Prepare and send the response
            response = {
                'result': result
            }
            
            # Write the response to stdout
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError:
            # Handle invalid JSON input
            print(json.dumps({'error': 'Invalid JSON input'}), flush=True)
        except Exception as e:
            # Handle other errors
            print(json.dumps({'error': str(e)}), flush=True)

if __name__ == '__main__':
    main() 