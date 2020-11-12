FROM debian

# Copying swapi project to the installation directory
WORKDIR /opt
COPY swapi/ swapi/

RUN apt-get -yqq update && \
    apt-get -yqq install -y --no-install-recommends apt-utils && \
    apt-get -yqq update && \
    apt-get -yqq upgrade

# installing python
RUN apt-get -yqq install python2 \
      python2-dev \
      python-pip

# installing needful tools
RUN apt-get -yqq install liblzma-dev \
       mlocate \
       locate \
       wget \
       tree \
       curl \
       sudo \
       libmemcached-dev \
       zlib1g-dev \
       procps \
       git-core \
       vim

RUN update-alternatives --install /usr/bin/python python /usr/bin/python2 1
WORKDIR /opt/swapi/

RUN make install
RUN make build
RUN make load_data

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

