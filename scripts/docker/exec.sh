docker run --gpus all \
     --rm -it --name flow_$(($RANDOM % 1000 + 1000)) \
     --shm-size=8g \
     -v $PWD:/src \
     flow bash