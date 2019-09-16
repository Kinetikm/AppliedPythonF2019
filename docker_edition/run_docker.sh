
docker build -t amigoml -f Dockerfile .

docker run -dit \
	--name my_ml_container  \
	-p 8989:8989 \
	-v ~:/workspace \
	amigoml

#docker attach #HERE_PLACE_HASH like f31ace341123b43a325823

# in docker container
# jupyter notebook --no-browser --port=8189 --ip 0.0.0.0 --allow-root

# on
# http://localhost:8189/