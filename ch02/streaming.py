# pip install vllm
# python streaming.py

import asyncio
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams

# Initialize the vLLM async streaming engine arguments
engine_args = AsyncEngineArgs(
    model="Qwen/Qwen2.5-0.5B",
    dtype="float16",
    tensor_parallel_size=1,      # Number of GPUs to use
    gpu_memory_utilization=0.9,  # GPU memory utilization
    max_num_batched_tokens=32768, # Maximum number of tokens to process in a batch
    max_num_seqs=256,           # Maximum number of sequences to process
    disable_log_requests=True,   # Disable request logging
    disable_log_stats=True,      # Disable stats logging
)

# Create the vLLM async streaming engine
engine = AsyncLLMEngine.from_engine_args(engine_args)

# Define the async function to generate text in streaming mode
async def generate_text(prompt: str, max_tokens: int = 100):
    try:
        # Define sampling parameters
        sampling_params = SamplingParams(
            temperature=0.0,
            max_tokens=max_tokens,
            stop=["\n"],  # Stop at newline
        )

        # Generate text
        request_id = "test-request"  # Unique ID for this request
        # Generate tokens in streaming mode
        results_generator = engine.generate(
            prompt=prompt,
            sampling_params=sampling_params,
            request_id=request_id
        )

        # Process the results
        final_output = None
        async for request_output in results_generator:
            final_output = request_output
            # Print each token as it's generated
            for output in request_output.outputs:
                print(output.text, end="", flush=True)
            print()  # Newline at the end of each output

        return final_output
    except asyncio.CancelledError:
        # Handle cancellation gracefully
        print("\nGeneration was cancelled")
        return None
    finally:
        # Always clean up
        try:
            await engine.abort(request_id)
        except:
            pass

# Example of the streamingusage:
prompt = "What is the capital of US?"
res = asyncio.run(generate_text(prompt))
print(res.outputs[0].text)