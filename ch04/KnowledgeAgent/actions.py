import logging
from typing import Dict, Any, Optional
from rag_system import RAGSystem
from llm_manager import LLMManager

logger = logging.getLogger(__name__)

class ActionExecutor:
    def __init__(self, rag_system: RAGSystem, llm_manager: LLMManager):
        self.rag_system = rag_system
        self.llm_manager = llm_manager
    
    def execute_action(self, action_name: str, query: str, context: str = "", 
                      user_profile: Optional[Dict[str, Any]] = None) -> str:
        """Execute a specific action based on the action name."""
        logger.info(f"Executing action: {action_name}")
        
        if action_name == "query_rag_with_context":
            return self.query_rag_with_context(query, context)
        elif action_name == "generate_profile_based_response":
            return self.generate_profile_based_response(query, context, user_profile)
        elif action_name == "generate_summary":
            return self.generate_summary(query, context)
        elif action_name == "generate_analysis":
            return self.generate_analysis(query, context)
        else:
            raise ValueError(f"Unknown action: {action_name}")
    
    def query_rag_with_context(self, query: str, context: str = "") -> str:
        """Query the LLM with context from RAG vector database."""
        logger.info("Executing query_rag_with_context action")
        
        # If no context provided, get it from RAG system
        if not context:
            context = self.rag_system.get_context_for_query(query)
        
        # Create RAG prompt
        rag_prompt = self.llm_manager.create_rag_prompt(query, context)
        
        # Generate response
        response = self.llm_manager.generate_response(rag_prompt)
        
        logger.info("Successfully generated RAG-based response")
        return response
    
    def generate_profile_based_response(self, query: str, context: str = "", 
                                      user_profile: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response based on the user's profile."""
        logger.info("Executing generate_profile_based_response action")
        
        # Use default profile if none provided
        if user_profile is None:
            from config import Config
            user_profile = Config.DEFAULT_USER_PROFILE
        
        # If no context provided, get it from RAG system
        if not context:
            context = self.rag_system.get_context_for_query(query)
        
        # Create profile-based prompt
        profile_prompt = self.llm_manager.create_profile_based_prompt(
            query, context, user_profile
        )
        
        # Generate response
        response = self.llm_manager.generate_response(profile_prompt)
        
        logger.info("Successfully generated profile-based response")
        return response
    
    def generate_summary(self, query: str, context: str = "") -> str:
        """Generate a summary of the retrieved information."""
        logger.info("Executing generate_summary action")
        
        # If no context provided, get it from RAG system
        if not context:
            context = self.rag_system.get_context_for_query(query)
        
        # Create summary prompt
        summary_prompt = self.llm_manager.create_summary_prompt(context, max_length=300)
        
        # Generate response
        response = self.llm_manager.generate_response(summary_prompt)
        
        logger.info("Successfully generated summary")
        return response
    
    def generate_analysis(self, query: str, context: str = "") -> str:
        """Generate a detailed analysis of the retrieved information."""
        logger.info("Executing generate_analysis action")
        
        # If no context provided, get it from RAG system
        if not context:
            context = self.rag_system.get_context_for_query(query)
        
        # Create analysis prompt
        analysis_prompt = self.llm_manager.create_analysis_prompt(query, context)
        
        # Generate response
        response = self.llm_manager.generate_response(analysis_prompt)
        
        logger.info("Successfully generated analysis")
        return response
    
    def get_action_description(self, action_name: str) -> str:
        """Get a description of what an action does."""
        descriptions = {
            "query_rag_with_context": "Query the knowledge base and generate a response based on retrieved context",
            "generate_profile_based_response": "Generate a personalized response based on the user's profile and retrieved context",
            "generate_summary": "Generate a concise summary of the retrieved information",
            "generate_analysis": "Generate a detailed analysis of the retrieved information"
        }
        return descriptions.get(action_name, "Unknown action")
    
    def validate_action_prerequisites(self, action_name: str) -> bool:
        """Validate that prerequisites are met for an action."""
        if action_name in ["query_rag_with_context", "generate_profile_based_response", 
                          "generate_summary", "generate_analysis"]:
            return len(self.rag_system.documents) > 0
        else:
            return False 