FROM python:3.12.2-slim-bullseye
WORKDIR / app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "manage.py", "runserver", "0.0.0:8000"]