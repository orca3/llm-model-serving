import json
import logging
from typing import List, Dict, Any
from llm_manager import LLMManager

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager
        self.available_actions = [
            "query_rag_with_context",
            "generate_profile_based_response",
            "generate_summary",
            "generate_analysis"
        ]
    
    def create_plan(self, query: str) -> Dict[str, Any]:
        """Create an execution plan for the given query using OpenAI."""
        logger.info(f"Creating plan for query: {query}")
        
        # Create planning prompt
        planning_prompt = self.llm_manager.create_planning_prompt(query, self.available_actions)
        
        # Get plan from OpenAI
        try:
            plan_response = self.llm_manager.generate_response(planning_prompt, temperature=0.3)
            
            # Parse JSON response
            plan = self._parse_plan_response(plan_response)
            
            logger.info(f"Created plan: {plan}")
            return plan
            
        except Exception as e:
            logger.error(f"Error creating plan: {str(e)}")
            # Fallback to default plan
            return self._create_fallback_plan(query)
    
    def _parse_plan_response(self, response: str) -> Dict[str, Any]:
        """Parse the OpenAI response to extract the plan."""
        try:
            # Try to extract JSON from the response
            response = response.strip()
            
            # Find JSON object in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                plan = json.loads(json_str)
                
                # Validate plan structure
                required_keys = ["plan", "reasoning", "estimated_steps"]
                if all(key in plan for key in required_keys):
                    return plan
                else:
                    raise ValueError("Plan missing required keys")
            else:
                raise ValueError("No JSON found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse plan response: {str(e)}")
            logger.warning(f"Raw response: {response}")
            raise
    
    def _create_fallback_plan(self, query: str) -> Dict[str, Any]:
        """Create a fallback plan when OpenAI planning fails."""
        logger.info("Creating fallback plan")
        
        # Simple heuristic-based planning
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["what", "how", "explain", "describe", "tell me"]):
            # Information-seeking query
            plan = {
                "plan": ["query_rag_with_context"],
                "reasoning": "User is asking for information, so we need to query the knowledge base",
                "estimated_steps": 1
            }
        elif any(word in query_lower for word in ["summarize", "summary", "brief"]):
            # Summary request
            plan = {
                "plan": ["query_rag_with_context", "generate_summary"],
                "reasoning": "User wants a summary, so we need to get context and then summarize",
                "estimated_steps": 2
            }
        elif any(word in query_lower for word in ["analyze", "analysis", "compare", "evaluate"]):
            # Analysis request
            plan = {
                "plan": ["query_rag_with_context", "generate_analysis"],
                "reasoning": "User wants analysis, so we need to get context and then provide detailed analysis",
                "estimated_steps": 2
            }
        else:
            # General query, use both actions
            plan = {
                "plan": ["query_rag_with_context", "generate_profile_based_response"],
                "reasoning": "General query requiring both knowledge retrieval and personalized response",
                "estimated_steps": 2
            }
        
        return plan
    
    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """Validate that the plan contains valid actions."""
        if not isinstance(plan, dict):
            return False
        
        if "plan" not in plan or not isinstance(plan["plan"], list):
            return False
        
        # Check if all actions in the plan are valid
        for action in plan["plan"]:
            if action not in self.available_actions:
                logger.warning(f"Invalid action in plan: {action}")
                return False
        
        return True
    
    def get_action_sequence(self, plan: Dict[str, Any]) -> List[str]:
        """Extract the action sequence from a plan."""
        if self.validate_plan(plan):
            return plan["plan"]
        else:
            logger.warning("Invalid plan, returning empty sequence")
            return [] 