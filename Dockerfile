FROM python:3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

#ENV PORT 8080

COPY ./app /app

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]

CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload