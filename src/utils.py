import json
import logging
from typing import Dict, List, Union

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def parse_llm_response(response: str) -> Dict[str, Union[str, List[str]]]:
    try:
        if isinstance(response, dict):
            return response
        
        # Clean response string
        response = response.strip().replace("```json", "").replace("```", "")
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "verdict": "Unverifiable",
            "evidence": [],
            "reasoning": "Could not parse LLM response"
        }