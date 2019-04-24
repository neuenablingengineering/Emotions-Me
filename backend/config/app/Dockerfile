FROM python:3.6.7

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

RUN mkdir /config
ADD config/app /config/

RUN pip install -r /config/requirements.txt

# install ffmpeg
RUN apt update && \
    apt install -y \ 
    ffmpeg 

# install AWS
RUN pip install awscli

# install S3FS
RUN apt install -y \
    build-essential \ 
    git \
    libfuse-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    mime-support \
    automake \
    libtool \
    pkg-config \
    libssl-dev

RUN git clone https://github.com/s3fs-fuse/s3fs-fuse && \
    cd s3fs-fuse/ && \
    ./autogen.sh && \
    ./configure --prefix=/usr --with-openssl && \
    make && \
    make install

RUN mkdir /app
WORKDIR /app
ADD app /app/

CMD ["sh", "/config/on-container-start.sh"]
