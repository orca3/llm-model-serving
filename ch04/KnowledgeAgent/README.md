# Knowledge Agent

A demonstration AI agent that showcases how model serving can be used to build intelligent agents. This Knowledge Agent uses OpenAI's API to create a Retrieval-Augmented Generation (RAG) system that can query and analyze information from PDF documents.

## Overview

The Knowledge Agent is a sample implementation that demonstrates:

- **Model Serving Integration**: Uses OpenAI's API as the model serving backend for all LLM operations
- **RAG System**: Implements a complete Retrieval-Augmented Generation pipeline
- **Intelligent Planning**: Uses LLM-based planning to determine optimal action sequences
- **Multi-Modal Actions**: Supports various actions like querying, summarizing, analyzing, and personalized responses
- **PDF Document Processing**: Automatically processes and embeds PDF files for knowledge retrieval

### What It Can Do

- **Document Querying**: Ask questions about content in your PDF files
- **Intelligent Planning**: Automatically determines the best approach to answer your questions
- **Personalized Responses**: Tailors responses based on user expertise level and background
- **Summarization**: Creates concise summaries of retrieved information
- **Analysis**: Provides detailed analysis of document content
- **Interactive Mode**: Simple command-line interface for easy interaction

This agent serves as a practical example of how to build AI agents using external model serving APIs, demonstrating best practices for RAG implementation, prompt engineering, and system architecture.

## System Design & Components

The Knowledge Agent is built with a modular architecture consisting of several key components:

### Core Components

1. **Agent** (`agent.py`): Main orchestrator that coordinates all components
2. **RAG System** (`rag_system.py`): Handles PDF processing, embeddings, and vector search
3. **LLM Manager** (`llm_manager.py`): Manages all OpenAI API interactions and token management
4. **Planner** (`planner.py`): Uses LLM to create intelligent execution plans
5. **Action Executor** (`actions.py`): Executes specific actions like querying, summarizing, etc.
6. **Configuration** (`config.py`): Centralized configuration management

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│     Agent       │───▶│   OpenAI API    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Components    │
                       │                 │
                       │ • RAG System    │
                       │ • LLM Manager   │
                       │ • Planner       │
                       │ • Actions       │
                       └─────────────────┘
```

### Dependencies

**Primary Dependency**: OpenAI API
- **LLM**: GPT-4 for planning and responses
- **Embeddings**: text-embedding-3-small for document embeddings
- **No Local Models**: All AI capabilities are served via API

**Other Dependencies**:
- `PyPDF2`: PDF text extraction
- `tiktoken`: Token counting and management
- `numpy`: Vector similarity calculations
- `python-dotenv`: Environment variable management

## Repository Structure

```
KnowledgeAgent/
├── agent.py                 # Main agent orchestrator
├── rag_system.py           # RAG system for document processing
├── llm_manager.py          # OpenAI API management
├── planner.py              # LLM-based planning system
├── actions.py              # Action execution logic
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from env_example.txt)
├── env_example.txt         # Example environment configuration
├── README.md               # This file
├── example_usage.py        # Example usage script
├── test_agent.py           # Test suite
├── test_rag_system.py      # RAG system tests
├── test_api_key.py         # API key validation test
├── debug_agent.py          # Debugging utilities
├── debug_simple.py         # Simple debugging script
├── DEBUG_GUIDE.md          # Debugging guide
├── knowledge_files/        # PDF documents for knowledge base
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
└── vector_db/              # Vector database storage (auto-generated)
```

## How to Run the Agent Locally

### Prerequisites

1. **Python 3.8+** installed on your system
2. **OpenAI API Key** with sufficient credits
3. **PDF files** to analyze (place in `knowledge_files/` directory)

### Step 1: Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd KnowledgeAgent

# Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Install dependencies in virtual environment
pip install -r requirements.txt

# Create environment file
cp env_example.txt .env

# Edit .env with your OpenAI API key
# OPENAI_API_KEY=your-actual-api-key-here
```

### Step 2: Add PDF Documents

```bash
# Place your PDF files in the knowledge_files directory
cp /path/to/your/documents/*.pdf knowledge_files/
```

### Step 3: Run the Agent

```bash
# Run in interactive mode
python agent.py
```

The agent will:
1. Load environment variables from `.env`
2. Build the knowledge base from PDF files
3. Start interactive mode where you can ask questions
4. Type 'quit' to exit

#### Example Queries to Try

Based on the included technical documents, here are some example queries that showcase the agent's capabilities:

**📚 Database & Data Mining Queries:**
- "What are the main types of database queries discussed in the tutorial?"
- "Explain the difference between OLAP and data mining techniques"
- "How do database queries relate to data mining processes?"
- "What are the key concepts in OLAP operations?"

**🔧 Intel 5-Level Paging Queries:**
- "What is 5-level paging and how does it work?"
- "Explain the Extended Page Tables (EPT) in Intel processors"
- "How does 5-level paging improve memory management?"
- "What are the benefits of 5-level paging over traditional paging?"

**🌳 Patricia Tries & Data Structures:**
- "What are Patricia tries and how are they optimized?"
- "Explain HTM-enabled dynamic data structures"
- "How do Patricia tries compare to other tree data structures?"
- "What optimization techniques are used in HTM-enabled structures?"

**📝 Standard Annotation Language (SAL):**
- "What is the Standard Annotation Language (SAL) used for?"
- "How does SAL help with code annotation and documentation?"
- "What are the key features of SAL?"
- "How does SAL improve software development processes?"

**🔍 Cross-Document Analysis:**
- "Compare the optimization techniques mentioned across all documents"
- "What are the common themes in these technical documents?"
- "How do these technologies relate to modern computing systems?"
- "Summarize the key innovations discussed in these papers"

**🎯 Advanced Capabilities:**
- "Analyze the performance implications of 5-level paging in modern systems"
- "Create a detailed comparison between database query optimization and data structure optimization"
- "Explain how these technologies could be applied in a real-world project"
- "What are the future implications of these technologies?"

### Alternative: Programmatic Usage

```python
from agent import Agent

# Initialize agent
agent = Agent()

# Build knowledge base
agent.build_knowledge_base()

# Process queries
result = agent.process_query("What is the main topic of the documents?")
print(result["final_response"])
```

## How to Run Tests

### Run All Tests

```bash
# Run the main test suite
python test_agent.py

# Run specific test files
python test_rag_system.py
python test_api_key.py
```

### Test Individual Components

```python
# Test RAG system
from rag_system import RAGSystem
rag = RAGSystem()
rag.build_vector_db()

# Test LLM manager
from llm_manager import LLMManager
llm = LLMManager()
response = llm.generate_response("Hello, world!")

# Test agent
from agent import Agent
agent = Agent()
status = agent.get_system_status()
```

### Test Configuration

```bash
# Validate API key
python test_api_key.py

# Check environment setup
python -c "from config import Config; print(Config().OPENAI_API_KEY[:10] + '...')"
```

## How to Debug the Agent

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Debug Scripts

```bash
# Run debug utilities
python debug_agent.py
```

### Using Python Debugger (pdb)

The Python debugger (pdb) is a powerful tool for debugging the agent. Here are some examples:

#### 1. Debug Agent Initialization

```python
import pdb
from agent import Agent

# Set breakpoint before agent creation
pdb.set_trace()
agent = Agent()
```

#### 2. Debug Query Processing

```python
import pdb
from agent import Agent

agent = Agent()
agent.build_knowledge_base()

# Debug the query processing step by step
def debug_query(query):
    pdb.set_trace()  # Breakpoint here
    result = agent.process_query(query)
    return result

debug_query("What is the main topic?")
```

#### 3. Debug RAG System

```python
import pdb
from rag_system import RAGSystem

rag = RAGSystem()

# Debug PDF loading
pdb.set_trace()
documents = rag.load_pdfs()
print(f"Loaded {len(documents)} documents")

# Debug vector search
pdb.set_trace()
results = rag.search("database queries", k=3)
```

#### 4. Debug LLM Manager

```python
import pdb
from llm_manager import LLMManager

llm = LLMManager()

# Debug token counting
pdb.set_trace()
tokens = llm.count_tokens("Your test text here")
print(f"Token count: {tokens}")

# Debug API call
pdb.set_trace()
response = llm.generate_response("Hello, world!")
```

#### 5. Common pdb Commands

When you hit a breakpoint, use these commands:

```bash
# Navigation
n (next)          # Execute the next line
s (step)          # Step into function calls
c (continue)      # Continue execution
q (quit)          # Quit debugger

# Inspection
p variable_name   # Print variable value
pp variable_name  # Pretty print variable
l (list)          # Show current code location
w (where)         # Show call stack

# Variable manipulation
!variable = value # Set variable value
dir(object)       # Show object attributes
```

#### 6. Debug with Conditional Breakpoints

```python
import pdb
from agent import Agent

agent = Agent()

def debug_with_condition(query):
    if len(query) > 50:  # Only debug long queries
        pdb.set_trace()
    result = agent.process_query(query)
    return result

# This will trigger the debugger
debug_with_condition("This is a very long query that should trigger the debugger")
```

### Common Debugging Scenarios

#### 1. API Key Issues

```python
# Test API key validity
from test_api_key import test_openai_api_key
test_openai_api_key()
```

#### 2. PDF Processing Issues

```python
# Debug PDF loading
from rag_system import RAGSystem
rag = RAGSystem()
documents = rag.load_pdfs()
print(f"Loaded {len(documents)} documents")
```

#### 3. Token Limit Issues

```python
# Check token usage
from llm_manager import LLMManager
llm = LLMManager()
tokens = llm.count_tokens("Your text here")
print(f"Token count: {tokens}")
```

#### 4. Vector Database Issues

```python
# Debug vector database
from rag_system import RAGSystem
rag = RAGSystem()
rag.build_vector_db()
print(f"Documents: {len(rag.documents)}")
print(f"Embeddings: {len(rag.embeddings)}")
```

### Debug Mode Features

The agent includes several debugging features:

- **Token Counting**: Monitor token usage to prevent context length exceeded errors
- **Context Validation**: Automatic validation of prompt lengths
- **Error Logging**: Detailed error messages and stack traces
- **System Status**: Get detailed status of all components
- **Step-by-Step Execution**: Trace through action sequences

### Troubleshooting Common Issues

1. **"Context length exceeded"**: Reduce `MAX_TOKENS` in config or use shorter queries
2. **"API key not found"**: Ensure `.env` file exists and contains valid API key
3. **"No documents found"**: Check that PDF files exist in `knowledge_files/`
4. **"Rate limit exceeded"**: Add delays between API calls or upgrade API plan

### Debug Guide

For detailed debugging instructions, see `DEBUG_GUIDE.md` in the repository.

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `LLM_MODEL` | `gpt-4` | LLM model for planning and responses |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Model for document embeddings |
| `MAX_TOKENS` | `2048` | Maximum tokens for responses |
| `TEMPERATURE` | `0.7` | Response creativity (0.0-1.0) |
| `CHUNK_SIZE` | `1000` | Text chunk size for embeddings |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |

### User Profile Configuration

```python
user_profile = {
    "expertise_level": "intermediate",  # beginner, intermediate, advanced
    "background": "technical",         # technical, business, academic
    "preferred_detail_level": "moderate"  # low, moderate, high
}
```

## Performance & Cost Considerations

- **Embeddings**: ~$0.01-0.05 per 1000 pages
- **LLM Calls**: ~$0.10-0.50 per query (depending on response length)
- **No Local Model Costs**: All processing done via API
- **Memory Usage**: Minimal RAM requirements (no local models)

## Security Notes

- Never commit `.env` files with API keys
- Use environment variables for sensitive data
- Monitor API usage and costs
- Consider API key rotation for production use

---

This Knowledge Agent demonstrates how to build intelligent AI agents using external model serving APIs, providing a practical example of RAG implementation and system architecture best practices. 