FROM pypy:3-slim

ENV PYTHONUNBUFFERED 1

ENV RUNTIME_PACKAGES \
    libev4

ENV BUILD_PACKAGES \
    build-essential \
    libev-dev \
    git

RUN apt-get update && apt-get --assume-yes upgrade && pip install wheel
RUN apt-get install --no-install-recommends --assume-yes $RUNTIME_PACKAGES $BUILD_PACKAGES

WORKDIR /application/msa_stemmers
ADD requirements /application/msa_stemmers/requirements
ADD requirements.txt /application/msa_stemmers
RUN pip install --no-cache-dir --src /usr/local/src -r requirements.txt
ADD . /application/msa_stemmers
RUN mkdir /application/log && mkdir /application/run

RUN apt-get remove --purge --assume-yes $BUILD_PACKAGES

RUN adduser --uid 1000 --home /application --disabled-password --gecos "" msa_stemmers && \
    chown -hR msa_stemmers: /application

USER msa_stemmers
RUN ["pypy3", "manage.py", "download_nltk"]
EXPOSE 8000

ENTRYPOINT ["pypy3", "manage.py"]
CMD ["gunicorn"]


