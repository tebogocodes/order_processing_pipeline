FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /app
WORKDIR $APP_DIR

COPY requirements.txt .
RUN pip install --no-cache-option -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]