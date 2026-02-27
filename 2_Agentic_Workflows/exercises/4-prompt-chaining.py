import os
from openai import OpenAI  # type: ignore
from dotenv import load_dotenv  # type: ignore

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(system_prompt, user_prompt, model="gpt-4.1-nano"):
    """Simple wrapper for OpenAI API calls"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def feedstock_analyst_agent(feedstock_name):
    # Analyze the hydrocarbon feed
    system_prompt = """You are a petrochemical expert analyzing hydrocarbon feedstocks. 
    Provide a concise analysis of the given feedstock, highlighting its key components and general suitability 
    for producing valuable refined products like gasoline, diesel, and kerosene.
    """
    user_prompt = f"Analyze the feedstock: {feedstock_name}"
    print(f"Analyzing feedstock: {feedstock_name}")
    return call_openai(system_prompt, user_prompt)

def distillation_planner_agent(feedstock_analysis):
    # Allocate through distillation tower
    system_prompt = """You are a refinery distillation tower operations planner. 
    Based on the provided feedstock analysis, estimate the potential percentage yields for major products 
    like gasoline, diesel, and kerosene. Be realistic."""
    user_prompt = f"Based on the following feedstock analysis, estimate potential distillation yields:\n{feedstock_analysis}"
    print("Planning distillation yields...")
    return call_openai(system_prompt, user_prompt)

    
def market_analyst_agent(product_list):
    # Analyze market conditions
    system_prompt = """You are an energy market analyst. For the following list of refined products, 
    provide a brief analysis of current market demand (high, medium, low) and general profitability trends."""
    user_prompt = f"Analyze the market for these refined products: {product_list}"
    print("Analyzing market conditions...")
    return call_openai(system_prompt, user_prompt)


def production_optimizer_agent(distillation_plan, market_data):
    # Recommend an optimal production plan
    system_prompt = """You are a refinery production optimization expert. Your goal is to recommend 
    a production strategy based on potential yields and current market conditions."""
    user_prompt = f"""
    Given the following potential distillation plan:
    --- DISTILLATION PLAN ---
    {distillation_plan}
    --- END DISTILLATION PLAN ---
    And the following market analysis:
    --- MARKET ANALYSIS ---
    {market_data}
    --- END MARKET ANALYSIS ---
    Please provide a concise recommendation on which products the refinery should prioritize or focus on 
    to maximize value, considering both the potential yield and market conditions.
    """
    print("Optimizing production plan...")
    return call_openai(system_prompt, user_prompt)


if __name__ == "__main__":
    current_feedstock = "West Texas Intermediate Crude"

    print(f"Processing feedstock: {current_feedstock}\n")

    analysis1 = feedstock_analyst_agent(current_feedstock)
    print(f"\n--- Feedstock Analysis ---\n{analysis1}\n")

    plan2 = distillation_planner_agent(analysis1)
    print(f"\n--- Distillation Plan ---\n{plan2}\n")

    market_info3 = market_analyst_agent(plan2)
    print(f"\n--- Market Analysis ---\n{market_info3}\n")

    final_recommendation4 = production_optimizer_agent(plan2, market_info3)
    print(f"\n--- OPTIMIZED PRODUCTION RECOMMENDATION ---\n{final_recommendation4}\n")
