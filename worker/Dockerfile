FROM python:3.14

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /worker

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /worker
