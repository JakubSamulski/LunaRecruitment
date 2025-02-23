FROM python:3.13-alpine
EXPOSE 8000

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

# Maybe in real world app don't use runserver in production and instead use gunicorn or uvicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
