FROM python:3.12-alpine3.21

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "src/run.py"]
