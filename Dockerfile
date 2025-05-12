FROM python:3.11-slim-buster

WORKDIR /app
COPY requirements.txt /app/

# RUN pip freeze > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]