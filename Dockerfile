FROM python:3.12.9-bullseye

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "src/run.py"]
