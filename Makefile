DOCKER = sudo docker
NAME = genderful

test:
	python -m unittest discover

build:
	$(DOCKER) build -t $(NAME) .

run:
	# note the 127.0.0.1 in the -p, to prevent Docker from exposing the port
	# $(DOCKER) rm -f $(NAME) && $(DOCKER) run --name $(NAME) -p 127.0.0.1:8081:8081 $(NAME)
	$(DOCKER) rm -f $(NAME) && $(DOCKER) run -it --name $(NAME) -p 127.0.0.1:8081:8081 $(NAME)
	# $(DOCKER) run -it --name $(NAME) -p 127.0.0.1:8081:8081 $(NAME)


rm_containers:
	$(DOCKER) ps -aq | xargs $(DOCKER) rm || true

venv:
	eval $(source venv/bin/activate)
