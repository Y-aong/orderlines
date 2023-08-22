FROM ubuntu
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN pwd

RUN apt-get update -y && apt-get install -y python3-pip python3-dev
RUN apt -y install libgl1-mesa-glx libglib2.0-dev

# 下载依赖
COPY ./requirements.txt /app/requirements.txt
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN pip3 install -r requirements.txt
RUN apt-get install -y gunicorn

# 设置时区
ENV TZ=Asia/Shanghai
ENV PYTHONPATH=/app:$PYTHONPATH

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezon
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install --upgrade pip
COPY ./src /app
COPY ./pyproject.toml /app
COPY ./README.MD /app
RUN ls
RUN python -m pip install --upgrade pip
RUN python -m pip install --editable .
RUN which orderlines
RUN which celery
