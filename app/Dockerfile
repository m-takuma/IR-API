FROM python:3.10.7-slim

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app
CMD ["uvicorn", "controller.main:app", "--reload", "--host", "0.0.0.0", "--port", "3000"]