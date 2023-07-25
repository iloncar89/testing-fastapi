FROM python:3.11-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r req.txt
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]