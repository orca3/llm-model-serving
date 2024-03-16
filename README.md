# llm-model-serving
Source code for video course: LLM Model Serving in action

## clone the repo
Git Large File Storage is used in this repo since it contains some large model files (200MB+). Please instal the [Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage) (such as `brew install git-lfs` for mac) before clone the repo. 

## Project Overview
* [labs](./labs/): hands-on lab materials for the course.
* [images](./images/README.md): instructions (on docker compose) to run the backend model serving service locally, this is required for the labs. 
* [serving](./serving/README.md): model inference service, a Python Flask based RESTful service, hosts all the public model inference API. This service also works as a web proxy which route the prediction requests to different predictors behind. 
* [precitor](./predictor/): examples of differnet model precitors, such as [TorchServe](./predictor/torchserve/README.md) and self-developed predictors.   
* [.github](./.github/README.md): CI/CD files, the configured github workflow will create new release, build docker image and push to dockerhub automatically. 