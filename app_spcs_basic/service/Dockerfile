FROM python:3-alpine

RUN mkdir /web
COPY index.html /web
COPY main.py /web

# default port is 8080
EXPOSE 8080

WORKDIR /web

CMD ["python", "main.py"]
