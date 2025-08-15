import logging
from typing import Dict, Any, Optional
from openai import OpenAI

from config import Config

logger = logging.getLogger(__name__)

class LLMManager:
    def __init__(self):
        self.config = Config()
        if not self.config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        logger.info("LLM Manager initialized")
    
    def generate_response(self, prompt: str, max_tokens: Optional[int] = None, 
                         temperature: Optional[float] = None) -> str:
        """Generate response using OpenAI."""
        if max_tokens is None:
            max_tokens = self.config.MAX_TOKENS
        if temperature is None:
            temperature = self.config.TEMPERATURE
            
        try:
            response = self.client.chat.completions.create(
                model=self.config.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def create_planning_prompt(self, query: str, available_actions: list) -> str:
        """Create a prompt for the planner to determine the best action sequence."""
        prompt = f"""
You are an intelligent planning agent. Given a user query and available actions, determine the best sequence of actions to fulfill the user's request.

User Query: {query}

Available Actions:
{chr(10).join([f"{i+1}. {action}" for i, action in enumerate(available_actions)])}

Please analyze the query and respond with a JSON object containing:
1. "plan": A list of action names to execute in sequence
2. "reasoning": Brief explanation of why this plan was chosen
3. "estimated_steps": Number of steps this plan will take

Example response format:
{{
    "plan": ["action1", "action2"],
    "reasoning": "This plan will...",
    "estimated_steps": 2
}}

Respond only with the JSON object:
"""
        return prompt
    
    def create_rag_prompt(self, query: str, context: str) -> str:
        """Create a prompt for RAG-based question answering."""
        prompt = f"""
You are a helpful assistant with access to a knowledge base. Use the provided context to answer the user's question accurately and comprehensively.

Context from Knowledge Base:
{context}

User Question: {query}

Instructions:
1. Answer the question based ONLY on the provided context
2. If the context doesn't contain enough information to answer the question, say so
3. Provide specific details and examples from the context when relevant
4. Cite the source documents when possible
5. Be clear and well-structured in your response

Answer:
"""
        return prompt
    
    def create_profile_based_prompt(self, query: str, context: str, user_profile: Dict[str, Any]) -> str:
        """Create a prompt that considers the user's profile for personalized responses."""
        expertise_level = user_profile.get("expertise_level", "intermediate")
        background = user_profile.get("background", "technical")
        detail_level = user_profile.get("preferred_detail_level", "moderate")
        
        prompt = f"""
You are a helpful assistant responding to a user with the following profile:
- Expertise Level: {expertise_level}
- Background: {background}
- Preferred Detail Level: {detail_level}

Context from Knowledge Base:
{context}

User Question: {query}

Instructions:
1. Tailor your response to the user's expertise level ({expertise_level})
2. Consider their background ({background}) when explaining concepts
3. Provide {detail_level} level of detail
4. Use appropriate terminology and examples for their expertise level
5. If they're a beginner, explain technical terms. If they're advanced, you can use more technical language
6. Answer based on the provided context

Personalized Answer:
"""
        return prompt
    
    def create_summary_prompt(self, text: str, max_length: int = 200) -> str:
        """Create a prompt for summarizing text."""
        prompt = f"""
Please summarize the following text in {max_length} words or less, maintaining the key points and technical accuracy:

{text}

Summary:
"""
        return prompt
    
    def create_analysis_prompt(self, query: str, context: str) -> str:
        """Create a prompt for detailed analysis."""
        prompt = f"""
You are an expert analyst. Please provide a detailed analysis of the following question based on the provided context.

Question: {query}

Context:
{context}

Please provide:
1. A comprehensive analysis
2. Key insights and findings
3. Relevant examples from the context
4. Any limitations or gaps in the available information

Analysis:
"""
        return prompt 