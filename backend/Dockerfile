FROM python:3.9-slim

WORKDIR /app

# Debug: List files in the working directory
RUN ls -la

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]