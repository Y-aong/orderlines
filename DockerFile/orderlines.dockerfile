FROM ubuntu
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN pwd

RUN apt-get update -y && apt-get install -y python3-pip python3-dev
RUN apt -y install libgl1-mesa-glx libglib2.0-dev

# 下载依赖
COPY ./src/requirement.txt /app/requirement.txt
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN pip3 install -r requirement.txt
RUN apt-get install -y gunicorn

# 设置时区
ENV TZ=Asia/Shanghai
ENV PYTHONPATH=/app:$PYTHONPATH

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezon
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY ./src /app
# 使用gunicorn
CMD ["gunicorn", "app:app", "-c", "/app/conf/gunicorn_config.py"]
