FROM python:3.14

# Установка зависимостей для графики и браузера
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    xvfb \
    fluxbox \
    x11vnc \
    novnc \
    websockify \
    fonts-liberation \
    fonts-noto-color-emoji \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Установка браузера
RUN apt-get update && apt-get install -y chromium \
    && rm -rf /var/lib/apt/lists/*

COPY /parser_app/requirements.txt parser_app/requirements.txt

RUN pip install -r parser_app/requirements.txt

RUN playwright install chromium

COPY parser_app /parser_app

COPY /task2 /task2

COPY /app/models /app/models
COPY /app/db /app/db
COPY /app/schemas /app/schemas

COPY /worker /worker

COPY /parser_app/entrypoint.sh /parser_app/entrypoint.sh
RUN chmod +x /parser_app/entrypoint.sh
RUN sed -i 's/\r$//' /parser_app/entrypoint.sh

EXPOSE 8000 6080

WORKDIR /parser_app
ENTRYPOINT ["/parser_app/entrypoint.sh"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
