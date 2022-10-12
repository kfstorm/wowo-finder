FROM python:3.10-alpine

WORKDIR /app
COPY templates ./templates
COPY *.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
VOLUME "/root/.wowo"
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]
