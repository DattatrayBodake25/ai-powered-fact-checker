import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict, Any
from src.claim_extractor import ClaimExtractor
from src.retriever import FactRetriever

# Load env variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class FactChecker:
    def __init__(self):
        self.extractor = ClaimExtractor()
        self.retriever = FactRetriever()
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.max_retries = 3  # For API reliability

    def _clean_response(self, response_text: str) -> str:
        """Clean the API response by removing markdown code blocks."""
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        return response_text.strip()

    def generate_verdict(self, claim: str, facts: List[str]) -> Dict[str, Any]:
        """Generate a fact-checking verdict using LLM."""
        prompt = f"""You are a fact-checking AI. Respond ONLY with valid JSON in this exact format:
{{
  "verdict": "True" | "False" | "Unverifiable",
  "evidence": ["list", "of", "relevant facts"],
  "reasoning": "Short explanation"
}}

CLAIM TO VERIFY:
"{claim}"

AVAILABLE FACTS:
{chr(10).join(f"- {fact}" for fact in facts)}
"""
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                cleaned_response = self._clean_response(response.text)
                return json.loads(cleaned_response)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return {
                        "verdict": "Unverifiable",
                        "evidence": [],
                        "reasoning": f"Error in verification: {str(e)}"
                    }

    def check(self, input_text: str) -> List[Dict[str, Any]]:
        """Main method to check facts in input text."""
        claims = self.extractor.extract_claim(input_text)
        results = []
        
        for claim in claims:
            facts = self.retriever.retrieve(claim)
            verdict_data = self.generate_verdict(claim, facts)
            
            results.append({
                "claim": claim,
                "verdict": verdict_data["verdict"].title(),
                "evidence": verdict_data["evidence"],
                "reasoning": verdict_data["reasoning"]
            })
        
        return results

if __name__ == "__main__":
    fc = FactChecker()
    input_text = "India conducted Operation Sindoor as a counter-terror mission in Jammu & Kashmir."
    output = fc.check(input_text)
    
    for item in output:
        print(f"Claim: {item['claim']}")
        print(f"Verdict: {item['verdict']}")
        print(f"Reasoning: {item['reasoning']}")
        print("Evidence:")
        for i, fact in enumerate(item['evidence'], 1):
            print(f"{i}. {fact}")
        print("=" * 50)