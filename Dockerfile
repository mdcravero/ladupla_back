# 
FROM python:3.9

# 
WORKDIR /code
ENV DB_USER: 'sqlserver'
ENV DB_PASS: 'cervantes'
ENV DB_NAME: 'ladupla'
ENV DB_HOST: '172.21.192.3'
ENV DB_PORT: 1433
#
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]