#Deriving the latest base image
FROM python:latest


# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY search.py ./

RUN apt update && apt install jq -y 

RUN pip install --upgrade pip && pip install -r requirements.txt