.PHONY: all build push deploy run stop

all: build push deploy

build:
	docker build -t 183878920773.dkr.ecr.us-east-2.amazonaws.com/emotions-and-me-backend:latest -f config/app/Dockerfile .

push:
	$(aws ecr get-login --no-include-email)
	docker push 183878920773.dkr.ecr.us-east-2.amazonaws.com/emotions-and-me-backend

deploy:
	eb deploy staging

run:
	docker-compose up -d

stop:
	docker-compose down
