FROM python:3.7.4


RUN mkdir -p /home/AMF_Evaluation_Metrics
WORKDIR /home/AMF_Evaluation_Metrics

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y git


ADD requirements.txt .
RUN pip install -r requirements.txt
RUN git clone https://github.com/Jacobe2169/GMatch4py
WORKDIR /home/AMF_Evaluation_Metrics/GMatch4py
RUN pip install .
WORKDIR /home/AMF_Evaluation_Metrics
RUN git clone  https://github.com/jfrelinger/cython-munkres-wrapper
WORKDIR /home/AMF_Evaluation_Metrics/cython-munkres-wrapper
RUN pip install .
WORKDIR /home/AMF_Evaluation_Metrics
RUN pip install gunicorn

ADD app app
ADD boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
