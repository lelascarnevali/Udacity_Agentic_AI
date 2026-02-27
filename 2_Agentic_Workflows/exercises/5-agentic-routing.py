import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(
    base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

# --- Helper Function for API Calls ---
def call_openai(system_prompt, user_prompt, model="gpt-4.1-nano"):
    """Simple wrapper for OpenAI API calls."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content


# --- Agents for Different Retail Tasks ---

def product_researcher_agent(query):
    """Product researcher agent gathers product information."""
    system_prompt = """You are a product research agent for a retail company. Your task is to provide 
    structured information about products, market trends, and competitor pricing. You MUST provide detailed 
    and accurate information that can help inform product development and pricing strategies."""
    
    user_prompt = f"Research this product thoroughly: {query}"
    print("Product Researcher Agent is processing the query...")
    return call_openai(system_prompt, user_prompt)


def customer_analyzer_agent(query):
    """Customer analyzer agent processes customer data and feedback."""
    system_prompt = """You are a customer analysis agent. Your task is to analyze customer feedback, 
    preferences, and purchasing patterns. You MUST provide insights that can help inform product development 
    and marketing strategies."""
    
    user_prompt = f"Analyze customer behavior for: {query}"
    print("Customer Analyzer Agent is processing the query...")
    return call_openai(system_prompt, user_prompt)


def pricing_strategist_agent(query, product_data=None, customer_data=None):
    """Pricing strategist agent recommends optimal pricing."""
    system_prompt = """You are a pricing strategist agent. Your task is to recommend optimal pricing 
    strategies based on product research and customer analysis."""
    
    # TODO: Implement this function
    # It should use product_data and customer_data to inform the pricing strategy

    user_prompt = f"""Original Pricing Query: {query}
                    Product Research Data:
                    {product_data}
                    Customer Analysis Data:
                    {customer_data}
                    Based on all the above information, please provide a recommended pricing strategy, 
                    suggest an optimal price or price range, and explain your reasoning.
                    """
    print("Pricing Strategist Agent is processing the query...")

    return call_openai(system_prompt, user_prompt)


# --- Routing Agent with LLM-Based Task Determination ---
def routing_agent(query, *args):
    """Routing agent that determines which agent to use based on the query."""
    


    # TODO: Implement the routing agent
    # 1. Use an LLM to analyze the query and determine the correct task type
    classification_system_prompt = """You are a helpful AI assistant that categorizes retail-related user queries. 
                                    Based on the user's query, determine if it is primarily about:
                                    * "product research" (e.g., asking for product specs, trends, competitor prices)
                                    * "customer analysis" (e.g., asking about customer feedback, preferences, 
                                    purchase patterns) * "pricing strategy" (e.g., asking for optimal pricing for a product)
                                    Respond only with one of these exact phrases: "product research", "customer analysis", 
                                    or "pricing strategy".
                                    """
    classification_user_prompt = f"Categorize this query: {query}"
    task_type = call_openai(classification_system_prompt, classification_user_prompt).strip()
    print(f"Query classified as: '{task_type}'")
    # 2. Route the query to the appropriate agent
    # 3. Return the results from the chosen agent
    if task_type == "product research":
        print("Routing to Product Researcher Agent...")
        return product_researcher_agent(query)
    elif task_type == "customer analysis":
        print("Routing to Customer Analyzer Agent...")
        return customer_analyzer_agent(query)
    elif task_type == "pricing strategy":
        print("Routing to Pricing Strategist Agent...")
        # For pricing strategy, we might want to gather additional data from the other agents
        product_data = product_researcher_agent(query)
        customer_data = customer_analyzer_agent(query)
        return pricing_strategist_agent(query, product_data, customer_data)
    else:
        print("Could not classify the query into a known task type.")
        return "Sorry, I couldn't determine the appropriate agent for this query."


# --- Example Usage ---
if __name__ == "__main__":
    # Example queries
    queries = [
        "What are the specifications and current market trends for wireless earbuds?",
        "What do customers think about our premium coffee brand?",
        "What should be the optimal price for our new organic skincare line?"
    ]
    
    # Process each query
    for query in queries:
        print(f"\nQuery: {query}")
        print("\nProcessing...")
        
        # TODO: Use the routing agent to process the query
        # Print the results
        print("-" * 30)
        result = routing_agent(query)
        print("\n--- ROUTING AGENT FINAL RESULT ---")
        print(result)
        print("=" * 30)