# nainstaluj Ubuntu 20.04 LTS
FROM ubuntu:20.04

# nastav jazyk
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# nastav apt
ARG DEBIAN_FRONTEND=noninteractive

###########################################
# Dependencies
###########################################
RUN apt update && apt install -y \
    curl \
    dialog \
    openssh-server \
    build-essential \
    python3 \
    python3-dev \
    graphviz \
    libglu1-mesa-dev \
    libgl1-mesa-dev \
    libosmesa6-dev \
    xvfb \
    ffmpeg \
    swig \
    && rm -rf /var/lib/apt/lists/*

# install pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN echo "$SSH_PASSWD" | chpasswd 
COPY docker/config/sshd_config /etc/ssh/

# install Web server
RUN python3 -m pip install gunicorn whitenoise

# set Django port
EXPOSE 8000 2222

# copy API's files
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python3 -m pip install -r requirements.txt --no-cache-dir
ADD . /code/

COPY docker/config/init.sh /usr/local/bin/
ENTRYPOINT [ "sh", "/usr/local/bin/init.sh" ]
