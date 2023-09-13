FROM python:3.11.4-alpine

WORKDIR /application

COPY requirements.txt /application/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /application

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
