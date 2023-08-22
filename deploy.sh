#!/bin/bash
version = "1.0.0.1"
docker build -f orderlines.dockerfile -t orderlines:${version} .
cd docker-compose
ENV_FILE="$PWD/.env"
echo "env file is $ENV_FILE"
if [ `grep -c "$PWD" $ENV_FILE` -ne '1' ];then
    echo "PROJECT_FILE_PATH=$PWD" >> .env
    echo "PROJECT_FILE_PATH=$PWD write complete!"
    exit 0
fi
docker-compose up -d
docker-compose ps