# Insurance Claims RAG System Exercise - Starter

from typing import Dict, List, Any, Optional, Union, Set
import importlib.util
import random
import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from pathlib import Path
from smolagents import (
    ToolCallingAgent,
    OpenAIServerModel,
    tool,
)
import os
import dotenv

# Note: Make sure to set up your .env file with your API key before running
dotenv.load_dotenv(dotenv_path='../.env')
openai_api_key = os.getenv('UDACITY_OPENAI_API_KEY')

model = OpenAIServerModel(
    model_id='gpt-4o-mini',
    api_base='https://openai.vocareum.com/v1',
    api_key=openai_api_key,
)

# Import core components from the demo file
# Note: In a real application, you would organize this better with proper imports
DEMO_FILE = (
    Path(__file__).resolve().parents[1]
    / 'demo'
    / '07-multi-agent-retrieval-augmented-generation-demo.py'
)
demo_spec = importlib.util.spec_from_file_location(
    'lesson07_multi_agent_rag_demo',
    DEMO_FILE,
)
if demo_spec is None or demo_spec.loader is None:
    raise ImportError(f'Could not load demo module from {DEMO_FILE}')

demo_module = importlib.util.module_from_spec(demo_spec)
demo_spec.loader.exec_module(demo_module)

PrivacyLevel = demo_module.PrivacyLevel
AccessControl = demo_module.AccessControl
Claim = demo_module.Claim
PatientRecord = demo_module.PatientRecord
ComplaintRecord = demo_module.ComplaintRecord
Database = demo_module.Database
VectorKnowledgeBase = demo_module.VectorKnowledgeBase
VectorClaimSearch = demo_module.VectorClaimSearch
DataGenerator = demo_module.DataGenerator
database = demo_module.database
vector_kb = demo_module.vector_kb
vector_claim_search = demo_module.vector_claim_search
search_knowledge_base = demo_module.search_knowledge_base
retrieve_claim_history = demo_module.retrieve_claim_history
get_claim_details = demo_module.get_claim_details
get_patient_info = demo_module.get_patient_info
find_similar_claims = demo_module.find_similar_claims
submit_complaint = demo_module.submit_complaint
respond_to_complaint = demo_module.respond_to_complaint
get_complaint_history = demo_module.get_complaint_history
process_new_claim = demo_module.process_new_claim
ClaimProcessingAgent = demo_module.ClaimProcessingAgent
CustomerServiceAgent = demo_module.CustomerServiceAgent
MedicalReviewAgent = demo_module.MedicalReviewAgent

"""
EXERCISE: CLAIM FRAUD DETECTION WITH RAG

In this exercise, you'll enhance the insurance claims processing system by adding 
fraud detection capabilities powered by RAG. Fraud detection is a critical component 
of insurance claims processing, saving the industry billions of dollars annually.

Your task is to:

1. Implement a FraudDetectionAgent class that leverages RAG to identify potentially 
   fraudulent claims by comparing them with known fraud patterns
   
2. Create a fraud knowledge base with common fraud indicators and patterns
   
3. Implement vector search functionality to identify similar fraud patterns
   
4. Integrate the agent into the existing workflow, adding a fraud review step to the
   claim processing pipeline

HINTS:
- You can use the existing VectorKnowledgeBase and VectorClaimSearch as references
- Your fraud detection component should consider multiple factors like claim frequency,
  unusual patterns, and similarity to known fraud cases
- Make sure to respect the privacy levels and access controls already in place
"""

# STEP 1: Create a knowledge base of fraud patterns
# TODO: Implement a fraud knowledge base with common fraud patterns
fraud_patterns = [
    {
        'topic': 'duplicate billing',
        'content': (
            'Repeated claims for the same patient, procedure code, and billing amount '
            'within a short time window can indicate duplicate billing or intentional '
            'resubmission of the same service.'
        ),
        'severity': 'high',
    },
    {
        'topic': 'claim frequency spike',
        'content': (
            'A sudden increase in claim frequency for the same patient over a period of '
            'days or weeks may indicate abuse, staged treatment plans, or coordinated fraud.'
        ),
        'severity': 'medium',
    },
    {
        'topic': 'unusual amount anomaly',
        'content': (
            'Claims with amounts that are far above the patients normal history or much '
            'higher than comparable claims for the same procedure should be reviewed.'
        ),
        'severity': 'high',
    },
    {
        'topic': 'repeat denied submissions',
        'content': (
            'Claims that repeat procedures or details from recently denied claims may signal '
            'attempts to resubmit fraudulent or unsupported treatments.'
        ),
        'severity': 'medium',
    },
    {
        'topic': 'copycat claim pattern',
        'content': (
            'A claim that is highly similar to several prior claims across the database can '
            'suggest a reused billing template or organized fraud behavior.'
        ),
        'severity': 'medium',
    },
]


def _parse_service_date(date_value: Optional[str]) -> Optional[datetime]:
    """Safely parse a YYYY-MM-DD service date."""
    if not date_value:
        return None

    try:
        return datetime.strptime(date_value, '%Y-%m-%d')
    except ValueError:
        return None


def _build_fraud_report(claim_id: str, access_level: str = PrivacyLevel.AGENT) -> Dict:
    """Build a deterministic fraud report for a claim."""
    claim = database.get_claim(claim_id, access_level)
    if not claim:
        return {
            'success': False,
            'error': 'Claim not found or access denied',
        }

    patient_id = claim.get('patient_id')
    patient = database.get_patient(patient_id, access_level) if patient_id is not None else None
    patient_history = database.get_patient_claims(patient_id, access_level) if patient_id is not None else []

    assessment = fraud_pattern_detector.detect_fraud_indicators(
        claim=claim,
        patient_history=patient_history,
        access_level=access_level,
    )

    return {
        'success': True,
        'claim_id': claim_id,
        'claim': claim,
        'patient': patient,
        'patient_history_count': max(len(patient_history) - 1, 0),
        **assessment,
    }

# STEP 2: Implement a vector-based fraud pattern detector
class FraudPatternDetector:
    def __init__(self):
        # TODO: Initialize the fraud detector with vector embeddings
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.patterns: List[Dict[str, Any]] = []
        self.pattern_vectors = None
        self.update_patterns(fraud_patterns)
        
    def update_patterns(self, fraud_patterns):
        # TODO: Update the patterns database
        self.patterns = fraud_patterns

        if not fraud_patterns:
            self.pattern_vectors = None
            return

        pattern_texts = [
            f"{pattern['topic']} {pattern['content']} {pattern.get('severity', '')}"
            for pattern in fraud_patterns
        ]
        self.pattern_vectors = self.vectorizer.fit_transform(pattern_texts)
        
    def detect_fraud_indicators(self, claim, patient_history, access_level=PrivacyLevel.AGENT):
        # TODO: Implement fraud detection logic
        # Use vector similarity and rule-based methods to identify potential fraud
        indicators: List[str] = []
        matched_patterns: List[Dict[str, Any]] = []
        risk_score = 0.0

        history_without_current = [
            historical_claim
            for historical_claim in patient_history
            if historical_claim.get('id') != claim.get('id')
        ]

        current_date = _parse_service_date(claim.get('service_date'))
        current_amount = float(claim.get('amount', 0.0) or 0.0)
        procedure_code = claim.get('procedure_code', '')
        procedure_description = database.procedure_codes.get(procedure_code, '')
        decision_reason = str(claim.get('decision_reason', '')).lower()

        if self.pattern_vectors is not None:
            history_summary = ' '.join(
                (
                    f"{historical_claim.get('procedure_code', '')} "
                    f"{historical_claim.get('status', '')} "
                    f"{historical_claim.get('decision_reason', '')}"
                )
                for historical_claim in history_without_current[:5]
            )
            query_text = (
                f"claim procedure {procedure_code} {procedure_description} "
                f"amount {current_amount} status {claim.get('status', '')} "
                f"reason {claim.get('decision_reason', '')} "
                f"patient history {len(history_without_current)} {history_summary}"
            )
            query_vector = self.vectorizer.transform([query_text])
            similarities = cosine_similarity(query_vector, self.pattern_vectors).flatten()

            for index, similarity in enumerate(similarities):
                if float(similarity) >= 0.12:
                    matched_patterns.append({
                        **self.patterns[index],
                        'similarity_score': round(float(similarity), 3),
                    })

            matched_patterns.sort(
                key=lambda pattern: pattern['similarity_score'],
                reverse=True,
            )

            if matched_patterns:
                top_match = matched_patterns[0]
                indicators.append(
                    f"Pattern match: {top_match['topic']} "
                    f"(similarity {top_match['similarity_score']:.2f})"
                )
                risk_score += min(0.25, 0.10 + top_match['similarity_score'] * 0.30)

        recent_claims: List[Dict[str, Any]] = []
        same_procedure_recent: List[Dict[str, Any]] = []
        exact_duplicates: List[Dict[str, Any]] = []
        denied_repeats = 0

        for historical_claim in history_without_current:
            historical_date = _parse_service_date(historical_claim.get('service_date'))
            if current_date and historical_date:
                days_difference = abs((current_date - historical_date).days)
                if days_difference <= 30:
                    recent_claims.append(historical_claim)
                    if historical_claim.get('procedure_code') == procedure_code:
                        same_procedure_recent.append(historical_claim)
                        historical_amount = float(historical_claim.get('amount', 0.0) or 0.0)
                        if abs(historical_amount - current_amount) < 1:
                            exact_duplicates.append(historical_claim)

            if (
                historical_claim.get('procedure_code') == procedure_code
                and str(historical_claim.get('status', '')).lower() == 'denied'
            ):
                denied_repeats += 1

        if len(recent_claims) >= 3:
            indicators.append(
                f"Patient submitted {len(recent_claims)} other claims within 30 days"
            )
            risk_score += 0.20

        if len(same_procedure_recent) >= 2:
            indicators.append(
                f"Procedure {procedure_code} repeated {len(same_procedure_recent)} times in 30 days"
            )
            risk_score += 0.25

        if exact_duplicates:
            indicators.append(
                f"Found {len(exact_duplicates)} near-duplicate claim(s) with same procedure and amount"
            )
            risk_score += 0.35

        history_amounts = [
            float(historical_claim.get('amount', 0.0) or 0.0)
            for historical_claim in history_without_current
            if historical_claim.get('amount') is not None
        ]
        average_historical_amount = (
            sum(history_amounts) / len(history_amounts)
            if history_amounts
            else 0.0
        )

        if (
            average_historical_amount > 0
            and current_amount >= average_historical_amount * 2.5
            and (current_amount - average_historical_amount) >= 150
        ):
            indicators.append(
                f"Claim amount ${current_amount:.2f} is unusually high compared with "
                f"patient average ${average_historical_amount:.2f}"
            )
            risk_score += 0.30

        if 'duplicate' in decision_reason or denied_repeats >= 2:
            indicators.append('Claim resembles prior denied or duplicate submissions')
            risk_score += 0.15

        if not vector_claim_search.is_initialized:
            vector_claim_search.update_claims(list(database.claims.values()))

        similar_claims = [
            result
            for result in vector_claim_search.search(claim, access_level, threshold=0.15)
            if result['claim'].get('id') != claim.get('id')
        ]

        if len(similar_claims) >= 4:
            indicators.append(
                f"Claim is highly similar to {len(similar_claims)} other claims in the database"
            )
            risk_score += 0.10

        risk_score = min(1.0, risk_score)

        if risk_score >= 0.75:
            risk_level = 'high'
            recommended_action = 'Escalate for manual fraud investigation before payment.'
        elif risk_score >= 0.45:
            risk_level = 'medium'
            recommended_action = 'Hold for enhanced review and request supporting documentation.'
        else:
            risk_level = 'low'
            recommended_action = 'Proceed with the standard claim review workflow.'

        return {
            'risk_score': round(risk_score, 3),
            'risk_level': risk_level,
            'high_risk': risk_level == 'high',
            'indicators': indicators,
            'matched_patterns': matched_patterns[:3],
            'similar_claims': similar_claims[:3],
            'recommended_action': recommended_action,
        }


fraud_pattern_detector = FraudPatternDetector()

# STEP 3: Implement a tool for fraud detection
@tool
def check_claim_for_fraud(claim_id: str, access_level: str = PrivacyLevel.AGENT) -> Dict:
    """
    Check a claim for potential fraud indicators.
    
    Args:
        claim_id: The claim ID to check
        access_level: The access level of the requester
        
    Returns:
        Dictionary containing fraud assessment results
    """
    # TODO: Implement this tool to check for fraud
    return _build_fraud_report(claim_id=claim_id, access_level=access_level)

# STEP 4: Create a FraudDetectionAgent
class FraudDetectionAgent(ToolCallingAgent):
    """Agent for detecting potential fraud in insurance claims."""
    def __init__(self, model: OpenAIServerModel):
        # TODO: Implement the fraud detection agent
        super().__init__(
            tools=[
                check_claim_for_fraud,
                get_claim_details,
                get_patient_info,
                retrieve_claim_history,
                find_similar_claims,
                search_knowledge_base,
            ],
            model=model,
            name='fraud_detector',
            description="""Agent responsible for fraud detection in insurance claims.
            You retrieve claim details, patient history, similar claims, and relevant
            knowledge before deciding whether a claim is suspicious.
            Escalate claims that show unusually high amounts, repeated submissions,
            duplicate patterns, or strong similarity to known fraud indicators.
            """,
        )
        self.access_level = PrivacyLevel.AGENT

    def assess_claim(self, claim_id: str, access_level: str = PrivacyLevel.AGENT) -> Dict:
        """Run the fraud assessment without requiring an LLM call."""
        return _build_fraud_report(claim_id=claim_id, access_level=access_level)

# STEP 5: Update the orchestrator to include fraud detection
# TODO: Modify ComplaintResolutionOrchestrator to include fraud detection in the workflow
class FraudAwareClaimOrchestrator:
    """Coordinates standard claim review with a fraud detection step."""

    def __init__(self, model: OpenAIServerModel):
        self.model = model
        self.claim_processor = ClaimProcessingAgent(model)
        self.medical_reviewer = MedicalReviewAgent(model)
        self.fraud_detector = FraudDetectionAgent(model)

    def review_claim(self, claim_id: str) -> Dict:
        """Run the claim through the fraud review step."""
        fraud_assessment = self.fraud_detector.assess_claim(claim_id)
        if not fraud_assessment.get('success', False):
            return fraud_assessment

        workflow_status = (
            'manual_fraud_review_required'
            if fraud_assessment.get('high_risk')
            else 'ready_for_standard_processing'
        )

        return {
            'success': True,
            'claim_id': claim_id,
            'workflow_status': workflow_status,
            'fraud_assessment': fraud_assessment,
        }

# STEP 6: Function to demonstrate the fraud detection capabilities
def demonstrate_fraud_detection():
    """
    Run a demonstration of the fraud detection capabilities.
    """
    # TODO: Implement a demonstration of the fraud detection feature
    suspicious_patient = PatientRecord(
        patient_id=9001,
        name='Jordan Example',
        policy_number='POL-90001',
        contact_info={
            'email': 'jordan.example@example.com',
            'phone': '555-900-1001',
            'address': '101 Example Ave, Risktown, ST 90001',
        },
    )
    safe_patient = PatientRecord(
        patient_id=9002,
        name='Taylor Sample',
        policy_number='POL-90002',
        contact_info={
            'email': 'taylor.sample@example.com',
            'phone': '555-900-1002',
            'address': '202 Sample Rd, Safetown, ST 90002',
        },
    )

    database.add_patient(suspicious_patient)
    database.add_patient(safe_patient)

    seeded_claims = [
        Claim(9001, '2024-07-10', '97110', 210.00),
        Claim(9001, '2024-07-18', '97110', 225.00),
        Claim(9001, '2024-07-22', '97110', 230.00),
        Claim(9002, '2024-07-11', '99214', 135.00),
    ]

    for claim in seeded_claims:
        claim.status = 'denied'
        claim.decision_reason = 'Insufficient documentation provided.'
        database.add_claim(claim)

    suspicious_claim = Claim(9001, '2024-07-25', '97110', 980.00)
    suspicious_claim.status = 'denied'
    suspicious_claim.decision_reason = 'Duplicate claim.'
    database.add_claim(suspicious_claim)

    safe_claim = Claim(9002, '2024-07-28', '99214', 145.00)
    safe_claim.status = 'approved'
    safe_claim.decision_reason = 'Meets coverage criteria.'
    database.add_claim(safe_claim)

    vector_claim_search.update_claims(list(database.claims.values()))

    orchestrator = FraudAwareClaimOrchestrator(model)
    suspicious_report = orchestrator.review_claim(suspicious_claim.id)
    safe_report = orchestrator.review_claim(safe_claim.id)

    for label, report in [
        ('Suspicious claim review', suspicious_report),
        ('Low-risk claim review', safe_report),
    ]:
        print(label)
        print(json.dumps(report, indent=2))
        print()

    return {
        'suspicious_report': suspicious_report,
        'safe_report': safe_report,
    }

if __name__ == '__main__':
    # Initialize and populate database
    print('Initializing and populating database...')
    DataGenerator.populate_database(num_patients=20, num_claims=50, num_complaints=10)
    print(f"Database contains {len(database.patients)} patients, {len(database.claims)} claims, and {len(database.complaints)} complaints")
    
    # Run the fraud detection demo
    print('\n=== Insurance Claim Fraud Detection Demo ===\n')
    demonstrate_fraud_detection()
