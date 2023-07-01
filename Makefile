DOCKER = docker
NAME = wetterkrank/genderful

build:
	$(DOCKER) build -t $(NAME) .

serve:
	# note the 127.0.0.1 in the -p, to prevent Docker from exposing the port
	$(DOCKER) rm -f $(NAME) && $(DOCKER) run -p 127.0.0.1:8081:8081 $(NAME)

shell:
	docker run -it --entrypoint=/bin/bash $(NAME)

rm_containers:
	$(DOCKER) ps -aq | xargs $(DOCKER) rm || true
