FROM python:3.13


RUN mkdir -p /home/AMF_Evaluation_Metrics
WORKDIR /home/AMF_Evaluation_Metrics

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y git


ADD requirements.txt .
ADD README.md .
RUN pip install -r requirements.txt
RUN git clone https://github.com/Jacobe2169/GMatch4py
# 3.12 removes distutils. Setuptools is now used instead as a (mostly) drop-in
# replacement. Setuptools brings build isolation though which needs a few
# tweaks to get working.
ADD gmatch4py-build-fix.patch .
RUN patch -fp1 < gmatch4py-build-fix.patch
WORKDIR /home/AMF_Evaluation_Metrics/GMatch4py
RUN pip install .
WORKDIR /home/AMF_Evaluation_Metrics
RUN git clone  https://github.com/jfrelinger/cython-munkres-wrapper
# See comment about GMatch4py above.
ADD cython-munkres-wrapper-build-fix.patch .
RUN patch -fp1 < cython-munkres-wrapper-build-fix.patch
WORKDIR /home/AMF_Evaluation_Metrics/cython-munkres-wrapper
RUN pip install .
WORKDIR /home/AMF_Evaluation_Metrics
RUN pip install gunicorn

ADD app app

ENV FLASK_APP app

ENV PYTHONUNBUFFERED=1

EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "app.routes:app"]
