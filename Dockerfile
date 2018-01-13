FROM python:3.6.4-alpine3.7

ENV PYTHONUNBUFFERED 1

ENV RUNTIME_PACKAGES \
    libev \
    pcre

ENV BUILD_PACKAGES \
    libev-dev \
    git \
    build-base \
    pcre-dev \
    gcc \
    linux-headers

RUN apk update && apk upgrade && pip install wheel
RUN apk --no-cache add --virtual build-deps $BUILD_PACKAGES && \
    apk --no-cache add $RUNTIME_PACKAGES

WORKDIR /application/msa_stemmers
ADD requirements /application/msa_stemmers/requirements
ADD requirements.txt /application/msa_stemmers
RUN pip install --no-cache-dir --src /usr/local/src -r requirements.txt
ADD . /application/msa_stemmers
RUN mkdir /application/log && mkdir /application/run

RUN apk del build-deps

RUN adduser -D -u 1000 msa_stemmers -h /application
RUN chown -hR msa_stemmers: /application

USER msa_stemmers
RUN ["python", "manage.py", "download_nltk"]
EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["gunicorn"]
