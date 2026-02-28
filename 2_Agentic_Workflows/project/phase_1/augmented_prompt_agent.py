from workflow_agents.base_agents import AugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

augmented_agent = AugmentedPromptAgent(openai_api_key, persona)

augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# The agent used general knowledge from the gpt-3.5-turbo LLM model to answer the prompt.
# By specifying the persona as a college professor, the system prompt caused the agent
# to adopt that role, starting the response with "Dear students," and framing the answer
# in an educational tone. Without the persona, the response would have been a plain factual answer.
