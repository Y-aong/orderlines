#!/bin/bash

declare -A repos
repos["orderlines"]="1.1.0"

mkdir -p repos
# iter repo
for key in "${!repos[@]}"; do
    echo "Key: $key, Value: ${repos[$key]}"
    # download repo
    git clone https://github.com/Y-aong/orderlines.git repos/${key}
    pushd repos/${key}
    git checkout ${repos[$key]}

    # build dockerfile
    for file in $(ls ./Dockerfile); do
    	name=${file%.dockerfile}
    	tag=${name}:${repos[$key]}
    	echo "docker build -t ${tag} -f ./Dockerfile/${file} ."
    	docker build -t ${tag} -f ./Dockerfile/${file} .

    	# save images
    	filepath=../../tar/${name}_${repos[$key]}.tar.gz
    	docker save -o $filepath $tag
    done

    popd
done
