# llm-model-serving
Code repository for book: "Serving and Optimizing LLMs", 


*Notes: Please instal the [Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage) (such as `brew install git-lfs` for mac) before clone the repo. This is because this repo contains some large model files (200MB+).*

## Table of Content

* **Chapter 1: Model serving introduction**
    * What is Model
    * What is Model Serving
    * Common Model Serving Paradigms
    * GPU vs CPU
    * Batch inferencing
    * Stream inferencing

* **Chapter 2 Large Language Model (LLM) Serving**
    * Large Language Model Concept
    * Large Language Model Use Cases
    * Common Large Language Model Serving Paradigms

Chapter 3 Model serving Best Practice and Case studies
Learn how to design and implement a model serving solution that fits your own needs from scratch.
3.1 Common Model Serving Design Principles
3.2 Implement Model Serving from Scratch
Model management, multiple endpoints, ….
3.3 Implement Model Serving with AWS SageMaker
3.4 Implement LLM model serving from Scratch
3.5 Implement LLM Model Serving with AWS SageMaker
3.6 Implement Multi-Agent System with LLM model from Scratch

Chapter 4 Performance Challenges when Serving LLMs 
Understand motivation and challenges for optimizing LLM models 
4.1 Why optimize LLMs serving
4.2 LLM model Architecture
4.3 Performance Measurement
4.4 Challenges:
4.4.1 Model Size
4.4.2 Batching
4.4.3 Attention Calculation
4.4.4 Parallelism
4.4.5 Evaluation

Chapter 5 Black Box Optimization Techniques
Learn the universal optimization techniques (regardless the LLM architecture) 
5.1 Quantization
5.2 Multi GPU and Hosts Inferencing
5.3 Hardware and Software Selection

Chapter 6 LLM Specific Optimization Techniques
Learn the optimization techniques that are specifically designed for Transformer based LLM models.
6.1 Optimize Batching 
6.1.1 Dynamic Batching
6.1.2 Continuous Batching
6.1.3 Chunked prefill
6.2 Optimize Attention Calculation
6.2.1 CUDA Kernel
6.3 Speculative Decoding
6.4 Parallelism Improvement
6.5 Optimization frameworks Overview 
6.5.1 FasterTransformer 
6.5.2 TensorRT LLM
6.5.3 DeepSpeed
6.5.4 vLLM
6.5.5 Llama cpp

Chapter 7 LLM Serving Optimization Best Practice and Case Study
Teach how to complete a model optimization project from scratch
7.1 Optimization Principles
7.2 Validation Metrics and Methods
7.3 Common LLM Optimization Workflow
7.4 Optimize a Mistra 7B model end-to-end.

Appendix A: Setup Local Labs with docker
Appendix B: Setup Google Colab Labs for GPU scenario
Appendix C: Understand Transformer Model with GPT2
Appendix D: Attention Calculation Deep Dive
Appendix E: vLLM Crash Course


## Lab Architecture 
We developed this lab to provide a practical, hands-on introduction to the fundamentals of model serving. Our goal is for you to understand the basic principles, which will help make sense of the more complex model serving frameworks and solutions used in real-world applications once you grasp these foundational concepts.

In this lab, we demonstrate the general serving paradigm — proxy and predictors — through three services: **inference service**, **torchserve predictor**, and **llm predictor**.

The [Inference service](./serving/README.md) acts as the public interface, handling all model serving requests. Depending on the type of request, it either processes it locally or forwards it to the appropriate backend predictor.

The [TorchServe predictor](./predictor/torchserve/README.md) exemplifies the integration of an existing solution, PyTorch serving, into our infrastructure, showcasing its application within our setup.

The [LLM Predictor](./predictor/llm/README.md) provides an example of a custom-developed predictor. It hosts a llama model that operates without the need for a GPU. Additionally, it offers two APIs: one for streaming and another for predictive request.

![service architecture](./labs/architecture.png)

To run the lab locally, please follow the [deployment](./images/README.md) instruction.

## Project Overview
* [labs](./labs/): hands-on lab materials for the course.
* [deployment](./images/README.md): instructions (on docker compose) to run the backend model serving service locally, this is required for the labs. 
* [serving](./serving/README.md): model inference service, a Python Flask based RESTful service, hosts all the public model inference API. This service also works as a web proxy which route the prediction requests to different predictors behind. 
* [precitor](./predictor/): different types of model predictors, such as [TorchServe](./predictor/torchserve/README.md) and self-developed predictors - [llm predictor](./predictor/llm/README.md). Each of the predictor represents a different way of serving models.
* [.github](./.github/BuildInstruction.md): CI/CD files, the configured github workflow will create new release, build docker image and push to dockerhub automatically. 

