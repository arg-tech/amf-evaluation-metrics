FROM python:3.13 AS builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# These patches are needed to build after upgrading to python 3.12.
ADD gmatch4py-build-fix.patch .
RUN git clone https://github.com/Jacobe2169/GMatch4py && \
    patch -fp1 < gmatch4py-build-fix.patch && \
    pip install ./GMatch4py

ADD cython-munkres-wrapper-build-fix.patch .
RUN git clone https://github.com/jfrelinger/cython-munkres-wrapper && \
    patch -fp1 < cython-munkres-wrapper-build-fix.patch && \
    pip install ./cython-munkres-wrapper

FROM python:3.13-slim

RUN useradd --create-home --uid 1000 appuser
WORKDIR /home/appuser

COPY --from=builder /opt/venv /opt/venv
COPY app app

USER appuser

ENV PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=app \
    PYTHONUNBUFFERED=1

EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "app.routes:app"]
