# Minimal LangChain Demo

This demo showcases a simple 3-step LangChain application that:

1. Takes user input (a topic or question)
2. Processes it through a language model chain
3. Returns a formatted response

## Components

- **Simple Chain**: A basic LangChain sequence that processes user input
- **LLM Integration**: Using OpenAI's API to power the language model
- **Prompt Template**: Formatting user input into an effective prompt

## Implementation Plan

1. Set up environment and requirements
2. Create the simple chain with prompt templates
3. Build a minimal demo interface
4. Test with sample inputs

## Files

- `requirements.txt`: Dependencies
- `langchain_demo.py`: Main code for the basic chain demo
- `enhanced_demo.py`: Demo for sequential chain processing
- `python_agent_demo.py`: Demo for Python code execution agent
- `web_search_demo.py`: Demo for web search and information extraction
- `document_qa_demo.py`: Demo for question answering on local documents
- `.env`: Environment variables for API keys (not committed to version control)
- no readme file is needed

## Environment Notes
- Running on Windows with PowerShell
- Python 3.x environment
- that means using ; instead of &&

## changes and fixes

1. Updated import from `from langchain.llms import OpenAI` to `from langchain_openai import OpenAI`
2. Added `langchain-openai` package to requirements.txt
3. Replaced `LLMChain` with the new RunnableSequence pattern (`prompt | llm`)
4. Changed method call from `chain.run()` to `chain.invoke()`
5. Updated prompt imports from `langchain.prompts` to `langchain_core.prompts`
6. Fixed outdated import paths due to LangChain reorganization
7. Created custom Python REPL tool implementation for agent demo compatibility

Note: The LangChain package underwent significant reorganization as of version 0.1.0+ with many core components moving to specialized packages like `langchain-core` and integrations moving to packages like `langchain-openai`.
