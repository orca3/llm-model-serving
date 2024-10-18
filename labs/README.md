# Lab

## Prerequisite
1. Run the lab services on your local by following the instructions [lab deployment](./../deployment/README.md).
2. Activate virtual environment
```sh
conda create -n lab python=3.11
conda activate lab

pip install -r requirements.txt

conda deactivate # deactivate the environment
```

## Lab Structure
[TODO]
1. Jupyter Notebooks
2. Postman 

## Prerequiste
The entire lab is design to run on a local computer (Mac or Linux) with [Docker](https://docs.docker.com/), **no GPU required**.

Among all the Docker options, we highly recommend [Docker Desktop](https://docs.docker.com/desktop/), please check out the install instructions [here](https://docs.docker.com/desktop/).  

## Run the model serving service
To play with the lab tutorials (and Juypter notebooks), we first need to run the backend model serving service first, which will handle all the model serving requests generated from the lab scripts. To get start:  
1. Move to the [images](./images/) folder and run 
```
docker-compose up
```
2. Verify service status

    1. Check compose and container status [TODO]
    2. Send Echo request to validate backend [TODO]


## Revoke the lab resources
Move to the [images](./images/) folder and run 
```
docker-compose down
```

Check all the docker containers are released. 
