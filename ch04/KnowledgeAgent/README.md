# PDF Knowledge Agent

A simplified AI agent that uses OpenAI's API for all operations including RAG (Retrieval Augmented Generation), embeddings, and LLM interactions. This agent can query information from PDF files using OpenAI's powerful models without any local model dependencies.

## Features

- **OpenAI API Only**: Uses OpenAI API for all LLM calls and embeddings - no local models
- **Simplified RAG System**: Embeds PDF files using OpenAI's text-embedding-3-small model
- **Intelligent Planning**: Uses GPT-4 to determine the best action sequence for queries
- **Multiple Actions**: Supports RAG queries, profile-based responses, summaries, and analysis
- **In-Memory Storage**: Simple and efficient vector storage in memory with JSON persistence
- **Simple Interactive Mode**: Basic command-line interface for querying
- **User Profiles**: Personalized responses based on expertise level and background
- **Minimal Dependencies**: Only essential packages for OpenAI API integration

## Architecture

The agent consists of several key components:

1. **RAG System** (`rag_system.py`): Handles PDF processing and OpenAI embeddings
2. **LLM Manager** (`llm_manager.py`): Manages all OpenAI API interactions
3. **Planner** (`planner.py`): Uses GPT-4 to create execution plans
4. **Action Executor** (`actions.py`): Executes specific actions using OpenAI
5. **Agent** (`agent.py`): Main orchestrator and interface

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp env_example.txt .env
   # Edit .env with your OpenAI API key
   ```

3. **Add PDF files to the knowledge folder**:
   ```bash
   # Place your PDF files in the knowledge/ directory
   ls knowledge/
   ```

## Configuration

### Environment Variables

Copy `env_example.txt` to `.env` and configure:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `LLM_MODEL`: LLM model to use (default: gpt-4)
- `EMBEDDING_MODEL`: Embedding model to use (default: text-embedding-3-small)
- `CHUNK_SIZE`: Size of text chunks for embedding (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `MAX_TOKENS`: Maximum tokens for responses (default: 4096)
- `TEMPERATURE`: Response creativity (default: 0.7)

### User Profile

Customize responses based on user expertise:

```python
custom_profile = {
    "expertise_level": "beginner",  # "beginner", "intermediate", "advanced"
    "background": "business",       # "technical", "business", "academic"
    "preferred_detail_level": "high"  # "low", "moderate", "high"
}
```

## Usage

### Interactive Mode

Run the agent in simple interactive mode:

```bash
python agent.py
```

This will:
1. Build the knowledge base from PDF files
2. Start interactive mode where you can ask questions
3. Type 'quit' to exit

### Programmatic Usage

```python
from agent import Agent

# Initialize agent
agent = Agent()

# Build knowledge base
agent.build_knowledge_base()

# Process a query
result = agent.process_query("What is 5-level paging?")

if result["success"]:
    print(result["final_response"])
else:
    print(f"Error: {result['final_response']}")

# Custom user profile
custom_profile = {
    "expertise_level": "beginner",
    "background": "business",
    "preferred_detail_level": "high"
}

agent = Agent(user_profile=custom_profile)
agent.build_knowledge_base()
result = agent.process_query("Explain database queries")
```

### Example Usage

Run the example script:

```bash
python example_usage.py
```

## Available Actions

The agent can perform these actions:

1. **query_rag_with_context**: Query knowledge base and generate responses
2. **generate_profile_based_response**: Personalized responses based on user profile
3. **generate_summary**: Create concise summaries of retrieved information
4. **generate_analysis**: Provide detailed analysis of retrieved information

## Knowledge Base Management

### Building the Knowledge Base

```python
agent = Agent()
agent.build_knowledge_base()  # Process PDFs and create embeddings
```

### Saving and Loading

```python
# Save knowledge base
agent.save_knowledge_base("my_kb.json")

# Load knowledge base
agent.load_knowledge_base("my_kb.json")
```

### Direct Search

```python
# Search knowledge base directly
results = agent.search_knowledge_base("database queries", k=5)
for result in results:
    print(f"Score: {result['score']:.4f}")
    print(f"Content: {result['content'][:100]}...")
```

## System Requirements

- Python 3.8+
- OpenAI API key with sufficient credits
- Internet connection for API calls
- Minimal RAM (no local model loading required)

## Cost Considerations

This agent uses OpenAI's API for:
- **Embeddings**: text-embedding-3-small (very cost-effective)
- **LLM Calls**: GPT-4 for planning and responses
- **PDF Processing**: Local processing, no API cost

Estimated costs for 1000 pages of PDF:
- Embeddings: ~$0.01-0.05
- LLM calls: ~$0.10-0.50 per query (depending on response length)

**No local model costs or GPU requirements!**

## Testing

Run the test suite to verify everything works:

```bash
python test_agent.py
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Ensure `OPENAI_API_KEY` is set in your `.env` file
   - Verify the API key is valid and has sufficient credits

2. **PDF Processing Errors**:
   - Ensure PDF files are not corrupted
   - Check file permissions
   - Verify PDF files are text-based (not scanned images)

3. **Memory Issues**:
   - Large PDFs may require significant RAM
   - Consider reducing `CHUNK_SIZE` for very large documents

4. **API Rate Limits**:
   - OpenAI has rate limits on API calls
   - Add delays between requests if needed

### Logging

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Reference

### Agent Class

- `__init__(user_profile=None)`: Initialize agent
- `build_knowledge_base(force_rebuild=False)`: Build vector database
- `process_query(query, use_planning=True)`: Process user query
- `search_knowledge_base(query, k=5)`: Direct search
- `save_knowledge_base(filepath)`: Save to file
- `load_knowledge_base(filepath)`: Load from file
- `update_user_profile(new_profile)`: Update user profile
- `get_system_status()`: Get system status
- `interactive_mode()`: Start simple interactive interface

### RAG System

- `load_pdfs(folder_path=None)`: Load PDF files
- `build_vector_db(force_rebuild=False)`: Build vector database
- `search(query, k=5)`: Search vector database
- `get_context_for_query(query, k=5)`: Get formatted context
- `save_vector_db(filepath)`: Save to file
- `load_vector_db(filepath)`: Load from file

## Performance Tips

1. **Batch Processing**: Process multiple PDFs at once
2. **Caching**: Save and reload knowledge base to avoid reprocessing
3. **Chunk Size**: Adjust `CHUNK_SIZE` based on document complexity
4. **API Optimization**: Use appropriate models for your use case

## Security

- Never commit your `.env` file with API keys
- Use environment variables for sensitive data
- Monitor API usage and costs
- Consider using API key rotation for production

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with OpenAI's powerful API
- Uses OpenAI's text-embedding-3-small for efficient embeddings
- Leverages GPT-4 for intelligent planning and responses 