FROM alpine:3.14
FROM python

WORKDIR /app
COPY requirements.txt /app
COPY src /app/src

RUN python -m pip install -r requirements.txt
EXPOSE 5000
CMD echo "Port exposed, starting server"
#CMD ["python", "src/entrypoint.py"]