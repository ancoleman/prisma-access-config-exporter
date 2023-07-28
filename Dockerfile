FROM python:3.9.15-slim
WORKDIR /app
VOLUME /resources
COPY /src/. .
RUN mkdir .panapi
RUN mkdir resources
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN chmod +x main.py
