#!/usr/bin/env python3
"""
Debug script for the Agent

This script allows you to debug specific parts of the agent functionality
by setting breakpoints and testing individual components.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import Agent
from rag_system import RAGSystem
from llm_manager import LLMManager
from planner import Planner
from actions import ActionExecutor
from config import Config

def debug_agent_initialization():
    """Debug agent initialization."""
    print("🔍 Debugging Agent Initialization")
    print("=" * 50)
    
    # Set breakpoint here to debug initialization
    breakpoint()  # This will pause execution here
    
    try:
        agent = Agent()
        print("✅ Agent initialized successfully")
        return agent
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return None

def debug_knowledge_base_building(agent):
    """Debug knowledge base building."""
    print("\n🔍 Debugging Knowledge Base Building")
    print("=" * 50)
    
    # Set breakpoint here to debug knowledge base building
    breakpoint()  # This will pause execution here
    
    try:
        agent.build_knowledge_base()
        print("✅ Knowledge base built successfully")
        
        # Check system status
        status = agent.get_system_status()
        print(f"📊 System Status: {status}")
        
    except Exception as e:
        print(f"❌ Error building knowledge base: {e}")

def debug_query_processing(agent, query: str = "What is artificial intelligence?"):
    """Debug query processing."""
    print(f"\n🔍 Debugging Query Processing: '{query}'")
    print("=" * 50)
    
    # Set breakpoint here to debug query processing
    breakpoint()  # This will pause execution here
    
    try:
        result = agent.process_query(query)
        print(f"✅ Query processed successfully")
        print(f"📋 Result: {result}")
        
        if result["success"]:
            print(f"🎯 Final Response: {result['final_response']}")
        else:
            print(f"❌ Error: {result['final_response']}")
            
    except Exception as e:
        print(f"❌ Error processing query: {e}")

def debug_rag_system(agent):
    """Debug RAG system directly."""
    print("\n🔍 Debugging RAG System")
    print("=" * 50)
    
    # Set breakpoint here to debug RAG system
    breakpoint()  # This will pause execution here
    
    try:
        # Test search
        results = agent.search_knowledge_base("artificial intelligence", k=3)
        print(f"✅ Search results: {len(results)} documents found")
        
        for i, result in enumerate(results):
            print(f"   Document {i+1}: {result['content'][:100]}...")
            print(f"   Score: {result['score']:.4f}")
            
    except Exception as e:
        print(f"❌ Error in RAG system: {e}")

def debug_planner(agent):
    """Debug planner functionality."""
    print("\n🔍 Debugging Planner")
    print("=" * 50)
    
    # Set breakpoint here to debug planner
    breakpoint()  # This will pause execution here
    
    try:
        query = "What is machine learning and how does it work?"
        plan = agent.planner.create_plan(query)
        print(f"✅ Plan created: {plan}")
        
        action_sequence = agent.planner.get_action_sequence(plan)
        print(f"📋 Action sequence: {action_sequence}")
        
    except Exception as e:
        print(f"❌ Error in planner: {e}")

def debug_actions(agent):
    """Debug action executor."""
    print("\n🔍 Debugging Action Executor")
    print("=" * 50)
    
    # Set breakpoint here to debug actions
    breakpoint()  # This will pause execution here
    
    try:
        query = "Explain database queries"
        result = agent.action_executor.query_rag_with_context(query)
        print(f"✅ Action executed successfully")
        print(f"📋 Result: {result[:200]}...")
        
    except Exception as e:
        print(f"❌ Error in action executor: {e}")

def main():
    """Main debug function."""
    print("🐛 Agent Debug Script")
    print("=" * 50)
    print("This script allows you to debug the agent step by step.")
    print("Set breakpoints in the functions above to pause execution.")
    print("=" * 50)
    
    # Debug initialization
    agent = debug_agent_initialization()
    if not agent:
        return
    
    # Debug knowledge base building
    debug_knowledge_base_building(agent)
    
    # Debug RAG system
    debug_rag_system(agent)
    
    # Debug planner
    debug_planner(agent)
    
    # Debug actions
    debug_actions(agent)
    
    # Debug query processing
    debug_query_processing(agent)
    
    print("\n🎉 Debug session completed!")

if __name__ == "__main__":
    main() 