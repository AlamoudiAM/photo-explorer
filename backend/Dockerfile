FROM python:3.7-slim-buster

RUN apt -y update

# video transcode
RUN apt install -y ffmpeg

# PostgresSQL
RUN apt install -y python3-dev python3-psycopg2

# Other
RUN apt install -y npm

# location where static is generated (on runtime - using django collectstatic)
VOLUME /app/collected_static

# install npm pkgs
# location is in '/npm_static' (one of the locations where django collectstatic search for statics)
WORKDIR /npm_static
COPY ./static/package.json ./
RUN npm install

# install backend python requirements
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
