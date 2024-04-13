FROM python:3.11

# Install ping and netcat for network troublehsooting
RUN apt-get update && apt-get install -y \
    iputils-ping \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /home/serving

COPY ./inference /home/serving/inference

WORKDIR /home/serving/inference

EXPOSE 80

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]