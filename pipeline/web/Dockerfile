FROM python:3-alpine
MAINTAINER Chris Weyandt <cweyandt@berkeley.edu> 

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
# WORKDIR /web

COPY ./pipeline/web/requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
# EXPOSE 5000

COPY ./pipeline/web/web_app.py /usr/src/app
COPY ./04_Website/* /usr/src/app

CMD [ "python", "web_app.py" ]

