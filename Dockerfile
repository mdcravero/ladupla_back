# 
FROM python:3.9

ENV PYTHONUNBUFFERED True
# 
WORKDIR /code
ENV DB_USER 'sqlserver'
ENV DB_PASS 'cervantes'
ENV DB_NAME 'ladupla'
ENV DB_HOST '172.21.192.3'
ENV DB_PORT 1433
ENV PORT 1234
#
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1