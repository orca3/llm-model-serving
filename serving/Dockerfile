FROM python:3.11

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /home/serving

COPY ./inference /home/serving/inference
WORKDIR /home/serving/inference

EXPOSE 80

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]