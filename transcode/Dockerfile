FROM jrottenberg/ffmpeg:vaapi

ENTRYPOINT [ "bash" ]

RUN apt update
RUN apt install -y python3 python3-pip

RUN pip3 install flask==1.1.2
WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8