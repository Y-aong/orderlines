#!/usr/bin/env sh

# 确保脚本抛出遇到的错误
set -e


git init
git add -A
git commit -m 'deploy'

git config --global user.name "Y-aong"
git config --global user.email "1627469727@qq.com"

# 填写你需要发布的仓库地址
git pull

cd -

