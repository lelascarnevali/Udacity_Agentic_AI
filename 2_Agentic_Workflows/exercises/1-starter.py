"""
Program Management Knowledge Agent - Starter Code

This program demonstrates two approaches to answering program management questions:
1. Using hardcoded knowledge
2. Using an LLM API

Complete the TODOs to build your knowledge agent.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

# TODO: Initialize the OpenAI client if API key is available
# Hint: Use os.getenv() to get the API key from environment variables
client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
) if os.getenv("OPENAI_API_KEY") else None

def get_hardcoded_answer(question):
    """
    Return answers to program management questions using hardcoded knowledge.
    
    Args:
        question (str): The question about program management
        
    Returns:
        str: The answer to the question
    """
    # TODO: Convert question to lowercase for easier matching
    question = question.lower()
    # TODO: Implement responses for at least 5 common program management questions
    # Include questions about: Gantt charts, Agile, sprints, critical path, and milestones
    if "gantt chart" in question:
        return "A Gantt chart is a visual representation of a project schedule, showing tasks, durations, and dependencies."
    elif "agile" in question:
        return "Agile is a project management methodology that emphasizes iterative development, collaboration, and flexibility."
    elif "sprint" in question:
        return "A sprint is a time-boxed period in Agile development during which specific work is completed and made ready for review."
    elif "critical path" in question:
        return "The critical path is the sequence of tasks that determines the minimum project duration."
    elif "milestone" in question:
        return "A milestone is a significant point or event in a project, often used to measure progress."
    # TODO: Add a default response for questions not in your knowledge base
    return "I'm sorry, I don't have an answer for that question."

def get_llm_answer(question):
    """
    Get answers to program management questions using an LLM API.
    
    Args:
        question (str): The question about program management
        
    Returns:
        str: The answer from the LLM
    """
    # TODO: Check if the LLM client is initialized
    try:
        if client is None:
            return "LLM API key not found. Please set the OPENAI_API_KEY environment variable."
    # Implement the API call to get an answer from the LLM
    # Use a system message to specify that the LLM should act as a program management expert
        else:
            response = client.chat.completions.create(
                model="gpt-5-nano",
                messages=[
                    {"role": "system", "content": "You are an expert assistant specializing in program management."},
                    {"role": "user", "content": question},
                ],
                # Nano requires reasoning_effort instead of text parameters
                extra_body={
                    "reasoning_effort": "minimal", # 'minimal' ensures lowest latency and cost
                    "verbosity": "low"             # Controls response length/detail in GPT-5
                }
            )

            return response.choices[0].message.content.strip()
    # TODO: Add error handling for API calls
    except Exception as e:
        return f"An error occurred while fetching the answer from the LLM: {e}"


# Demo function to compare both approaches
def compare_answers(question):
    """Compare answers from both approaches for a given question."""
    print(f"\nQuestion: {question}")
    print("-" * 50)
    
    # TODO: Get and display the hardcoded answer
    print("Hardcoded Answer:")
    print(get_hardcoded_answer(question))
    # TODO: Get and display the LLM answer (or a placeholder message)
    print("LLM Answer:")
    print(get_llm_answer(question))
    print("=" * 50)

# Demo with sample questions
if __name__ == "__main__":
    print("PROGRAM MANAGEMENT KNOWLEDGE AGENT DEMO")
    print("=" * 50)
    
    # TODO: Create a list of sample program management questions
    sample_questions = [
        "What is a Gantt chart?",
        "Tell me about Agile methodology.",
        "What are key project milestones?",
        "What is risk management in projects?", 
        "Can you explain a sprint review?"
    ]


    # TODO: Loop through the questions and compare answers

    for question in sample_questions:
        compare_answers(question)