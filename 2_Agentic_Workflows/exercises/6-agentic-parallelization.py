import os
from openai import OpenAI
from dotenv import load_dotenv
import threading

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(
    base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

# Shared dict for thread-safe collection of agent outputs
agent_outputs = {}

# Example contract text (in a real application, this would be loaded from a file)
contract_text = """
CONSULTING AGREEMENT

This Consulting Agreement (the "Agreement") is made effective as of January 1, 2025 (the "Effective Date"), by and between ABC Corporation, a Delaware corporation ("Client"), and XYZ Consulting LLC, a California limited liability company ("Consultant").

1. SERVICES. Consultant shall provide Client with the following services: strategic business consulting, market analysis, and technology implementation advice (the "Services").

2. TERM. This Agreement shall commence on the Effective Date and shall continue for a period of 12 months, unless earlier terminated.

3. COMPENSATION. Client shall pay Consultant a fee of $10,000 per month for Services rendered. Payment shall be made within 30 days of receipt of Consultant's invoice.

4. CONFIDENTIALITY. Consultant acknowledges that during the engagement, Consultant may have access to confidential information. Consultant agrees to maintain the confidentiality of all such information.

5. INTELLECTUAL PROPERTY. All materials developed by Consultant shall be the property of Client. Consultant assigns all right, title, and interest in such materials to Client.

6. TERMINATION. Either party may terminate this Agreement with 30 days' written notice. Client shall pay Consultant for Services performed through the termination date.

7. GOVERNING LAW. This Agreement shall be governed by the laws of the State of Delaware.

8. LIMITATION OF LIABILITY. Consultant's liability shall be limited to the amount of fees paid by Client under this Agreement.

9. INDEMNIFICATION. Client shall indemnify Consultant against all claims arising from use of materials provided by Client.

10. ENTIRE AGREEMENT. This Agreement constitutes the entire understanding between the parties and supersedes all prior agreements.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
"""

# TODO: Implement these agent classes

class LegalTermsChecker:
    """Agent that checks for problematic legal terms and clauses in contracts."""
    def run(self, contract_text):
        print("Running LegalTermsChecker...")
        # TODO: Implement this method to analyze legal terms
        system_prompt = """You are a legal expert specializing in contract law. 
                        Identify any problematic legal terms or clauses in the following contract text and 
                        explain why they may be an issue. You MUST provide specific feedback on each 
                        identified term or clause."""
        user_prompt = f"Please analyze the following contract text:\n\n{contract_text}"
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2)
        agent_outputs["legal"] = response.choices[0].message.content
        return agent_outputs

class ComplianceValidator:
    """Agent that validates regulatory and industry compliance of contracts."""
    def run(self, contract_text):
        print("Running ComplianceValidator...")
        # TODO: Implement this method to check compliance
        system_prompt = """You are a compliance expert with deep knowledge of industry regulations and standards. 
                        Analyze the following contract text for any potential compliance issues with relevant 
                        regulations and industry standards. Provide a detailed report of any identified 
                        compliance risks and suggest how to mitigate them."""
        user_prompt = f"Please analyze the following contract text:\n\n{contract_text}"
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2)
        agent_outputs["compliance"] = response.choices[0].message.content
        return agent_outputs

class FinancialRiskAssessor:
    """Agent that assesses financial risks and liabilities in contracts."""
    def run(self, contract_text):
        print("Running FinancialRiskAssessor...")
        # TODO: Implement this method to evaluate financial risks
        system_prompt = """You are a financial expert specializing in risk assessment. 
                        Analyze the following contract text for any potential financial risks, 
                        liabilities, or obligations that could impact the financial health of the parties involved. 
                        Provide a detailed report of any identified financial risks and suggest how to mitigate them."""
        user_prompt = f"Please analyze the following contract text:\n\n{contract_text}"
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[  
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2)
        agent_outputs["financial"] = response.choices[0].message.content
        return agent_outputs

class SummaryAgent:
    """Agent that synthesizes findings from all specialized agents."""
    def run(self, contract_text, inputs):
        # TODO: Implement this method to create a comprehensive summary
        print("SummaryAgent: Synthesizing all findings...")
        legal_findings = inputs.get("legal", "No legal analysis provided.")
        compliance_findings = inputs.get("compliance", "No compliance analysis provided.")
        financial_findings = inputs.get("financial", "No financial analysis provided.")
        system_prompt = """You are a senior legal counsel. You have received analyses on a contract from
                        legal terms, compliance, and financial risk specialists. Your task is to synthesize 
                        these findings into a single, comprehensive executive summary of the contract's overall 
                        status and key concerns."""
        
        user_prompt = f"""Please synthesize the following analyses of a contract into a comprehensive summary report.
            Original Contract Text (for reference, if needed, but focus on the analyses):
            --- BEGIN CONTRACT TEXT (abbreviated for prompt, or just mention it was analyzed) ---
            {contract_text[:500]}... 
            --- END CONTRACT TEXT ---
            Legal Terms Analysis:
            {legal_findings}
            Compliance Validation:
            {compliance_findings}
            Financial Risk Assessment:
            {financial_findings}
            Provide a consolidated executive summary identifying key issues and an overall assessment.
            """
        print("="*50)
        print("Legal Agent:\n ", legal_findings)
        print("="*50)
        print("Compliance Agent:\n ", compliance_findings)
        print("="*50)
        print("Financial Agent:\n ", financial_findings)
        print("="*50)

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3)
        return response.choices[0].message.content

# Main function to run all agents in parallel
def analyze_contract(contract_text):
    """Run all agents in parallel and summarize their findings."""
    # TODO: Implement parallel execution of agents
    # 1. Create agent instances
    legal_checker = LegalTermsChecker()
    compliance_validator = ComplianceValidator()
    financial_assessor = FinancialRiskAssessor()
    summary_creator = SummaryAgent()
    # 2. Run them in parallel using threading
    threads = [
        threading.Thread(target=legal_checker.run, args=(contract_text,)),
        threading.Thread(target=compliance_validator.run, args=(contract_text,)),
        threading.Thread(target=financial_assessor.run, args=(contract_text,))
        ]
    # 3. Collect their outputs
    for t in threads:
        t.start()
    for t in threads:        
        t.join()
    # 4. Generate a summary using the SummaryAgent
    final_report = summary_creator.run(contract_text, agent_outputs)
    # 5. Return the final analysis
    return final_report

if __name__ == "__main__":
    print("Enterprise Contract Analysis System")
    print("Analyzing contract...")
    
    # TODO: Call the analyze_contract function and print results
    final_analysis = analyze_contract(contract_text)
    print("\n=============== FINAL CONTRACT ANALYSIS ===============\n")
    print(final_analysis)