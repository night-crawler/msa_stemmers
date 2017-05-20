FROM python:3-alpine
RUN apk update && apk upgrade
RUN pip install wheel

WORKDIR /application/msa_stemmers
ADD requirements.txt /application/msa_stemmers
RUN pip install -r requirements.txt

ADD . /application/msa_stemmers
RUN mkdir /application/log && mkdir /application/run

RUN adduser -D -u 1000 msa_stemmers -h /application
RUN chown -hR msa_stemmers: /application

USER msa_stemmers
EXPOSE 17920

ENTRYPOINT ["python", "manage.py"]
CMD ["gunicorn"]
