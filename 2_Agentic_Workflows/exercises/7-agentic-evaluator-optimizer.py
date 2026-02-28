import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(
    base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

MAX_RETRIES = 5

# Example user constraints
RECIPE_REQUEST = {
    "base_dish": "pasta",
    "constraints": [
        "gluten-free",
        "vegan",
        "under 500 calories per serving",
        "high protein (>15g per serving)",
        "no coconut",
        "taste must be rated 7/10 or higher"
    ]
}

class RecipeCreatorAgent:
    """Agent that generates a recipe based on user constraints."""
    def create_recipe(self, recipe_request_dict, feedback=None):
        system_message = (
            "You are an innovative and highly skilled chef, renowned for creating "
            "delicious recipes that also meet specific dietary and nutritional targets. "
            "You are good at interpreting user requests and also at refining your "
            "creations based on precise feedback.\n\n"
            "IMPORTANT OUTPUT RULES:\n"
            "- Output ONLY the recipe content in the structured format requested.\n"
            "- Do NOT include conversational filler, greetings, or follow-up questions "
            "(e.g., no 'Absolutely!', no 'Would you like me to adjust...').\n"
            "- Start directly with the recipe name."
        )

        base_dish = recipe_request_dict['base_dish']
        constraints_str = ", ".join(recipe_request_dict['constraints'])
        user_prompt_text = f"Create a '{base_dish}' recipe that meets ALL of the following constraints: {constraints_str}."
        if feedback:
            user_prompt_text += (
                f"\n\nIMPORTANT: Your previous attempt had issues. "
                f"Please revise the recipe based on this specific feedback:\n{feedback}\n"
                f"Ensure all original constraints AND this feedback are addressed."
            )
        else:
            user_prompt_text += "\nThis is the first attempt."
        user_prompt_text += (
            "\n\nProvide EXACTLY these sections:\n"
            "1. **Name:** A creative name for the dish\n"
            "2. **Ingredients:** A list with quantities\n"
            "3. **Instructions:** Step-by-step\n"
            "4. **Estimated Calories:** per serving (number)\n"
            "5. **Estimated Protein:** grams per serving (number)\n"
            "6. **Taste Profile:** A short description"
        )
        print(f"\n👩‍🍳 Generating recipe with prompt:\n{user_prompt_text}\n")
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt_text}
            ],
            temperature=0.7
        )
        recipe = response.choices[0].message.content
        print(f"\n🍽️ Chef's creation:\n{recipe}\n")
        return recipe


class NutritionEvaluatorAgent:
    """Agent that evaluates a recipe against nutritional and dietary constraints."""

    def evaluate(self, recipe_details_str, original_request_dict):
        system_message = (
            "You are an extremely precise nutrition and dietary compliance evaluator.\n\n"
            "PROCESS — For EACH constraint you MUST follow these two steps:\n"
            "  Step 1 (REASONING): Compare the recipe's actual value to the constraint threshold. "
            "Write your comparison explicitly (e.g., '16g > 15g').\n"
            "  Step 2 (VERDICT): Based ONLY on the reasoning above, write PASSED or FAILED.\n\n"
            "STRICT RULES:\n"
            "- NEVER write the VERDICT before the REASONING.\n"
            "- If the numeric value meets or exceeds the threshold, the verdict is PASSED. "
            "Example: 16g protein > 15g requirement → PASSED.\n"
            "- Judge based on what the recipe ACTUALLY contains, not hypothetical concerns. "
            "Nutritional yeast IS vegan. Standard plant ingredients ARE gluten-free unless stated otherwise.\n"
            "- 'Overall Status' MUST be logically consistent: if ANY VERDICT is FAILED, "
            "Overall Status MUST be FAILED.\n"
            "- Use ONLY the exact output format specified. No extra commentary."
        )

        constraints = original_request_dict['constraints']
        num_constraints = len(constraints)
        numbered_constraints = '\n'.join(
            f"  {i+1}. {c}" for i, c in enumerate(constraints)
        )

        user_prompt_text = (
            f"Evaluate the following RECIPE against the specified constraints.\n\n"
            f"RECIPE:\n{recipe_details_str}\n\n"
            f"CONSTRAINTS TO EVALUATE ({num_constraints} total — you MUST evaluate ALL {num_constraints}):\n"
            f"{numbered_constraints}\n\n"
            f"OUTPUT FORMAT — For each constraint, write exactly TWO lines:\n"
            f"REASONING: <constraint> — <recipe value> vs <threshold>. <value> <comparison operator> <threshold> = <true/false>.\n"
            f"VERDICT: <constraint verbatim>: PASSED\n"
            f"or\n"
            f"VERDICT: <constraint verbatim>: FAILED - <reason>. <fix suggestion>.\n\n"
            f"=== FEW-SHOT EXAMPLES ===\n\n"
            f"REASONING: high protein (>15g per serving) — Recipe estimates 16g per serving. 16g > 15g = true.\n"
            f"VERDICT: high protein (>15g per serving): PASSED\n\n"
            f"REASONING: under 500 calories per serving — Recipe estimates 650 kcal. 650 < 500 = false.\n"
            f"VERDICT: under 500 calories per serving: FAILED - Estimated 650 calories. Suggest reducing oil by half.\n\n"
            f"REASONING: no coconut — Recipe ingredients do not include coconut in any form.\n"
            f"VERDICT: no coconut: PASSED\n\n"
            f"=== END EXAMPLES ===\n\n"
            f"After evaluating ALL {num_constraints} constraints, you MUST write this MANDATORY line:\n"
            f"Taste Rating: <N>/10\n\n"
            f"SELF-CHECK: Re-read all VERDICT lines above. Count how many say FAILED.\n"
            f"If count == 0, write: Overall Status: PASSED\n"
            f"If count >= 1, write: Overall Status: FAILED"
        )

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt_text}
            ],
            temperature=0.0
        )
        evaluation = response.choices[0].message.content
        print(f"\n🔍 Nutritionist's critique:\n{evaluation}\n")
        return evaluation

def optimize_recipe():
    current_feedback = None
    recipe_creator = RecipeCreatorAgent()
    evaluator = NutritionEvaluatorAgent()

    for attempt in range(MAX_RETRIES):
        print(f"\n--- Attempt {attempt + 1} of {MAX_RETRIES} ---")
        current_recipe_str = recipe_creator.create_recipe(RECIPE_REQUEST, current_feedback)
        print(f"💡 Chef Proposed:\n{current_recipe_str}")
        evaluation_str = evaluator.evaluate(current_recipe_str, RECIPE_REQUEST)
        print(f"🧐 Critic's Evaluation:\n{evaluation_str}")

        if "overall status: passed" in evaluation_str.lower():
            print("\n✅ Recipe Approved by Evaluator!")
            return current_recipe_str, evaluation_str, attempt + 1

        current_feedback = evaluation_str
        print("Recipe needs revision. Relaying feedback to Chef...")

    print(f"\n❌ Failed to meet all constraints after {MAX_RETRIES} attempts.")
    return current_recipe_str, evaluation_str, MAX_RETRIES


if __name__ == "__main__":
    print("Starting AI Recipe Optimizer Workflow...")
    final_recipe, final_evaluation, total_attempts = optimize_recipe()

    print("\n" + "=" * 60)
    if "overall status: passed" in final_evaluation.lower():
        print(f"🎉 OUTCOME: Approved after {total_attempts} attempt(s)!")
    else:
        print(f"😔 OUTCOME: Not approved after {total_attempts} attempt(s).")
    print(f"\n📋 FINAL RECIPE:\n{final_recipe}")
    print(f"\n📊 FINAL EVALUATION:\n{final_evaluation}")
