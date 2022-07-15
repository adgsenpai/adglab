FROM ubuntu:20.04

LABEL Maintainer="adgsenpai"

COPY . . 

RUN apt-get update 

RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["gunicorn","app:app","--bind","0.0.0.0:3000"]