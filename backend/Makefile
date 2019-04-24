.PHONY: all build push deploy run stop

all: build push deploy

build:
	docker build -t 806941466555.dkr.ecr.us-east-1.amazonaws.com/emotions-and-me-backend:latest -f config/app/Dockerfile .

push:
	$(aws ecr get-login --no-include-email)
	docker push 806941466555.dkr.ecr.us-east-1.amazonaws.com/emotions-and-me-backend

deploy:
	eb deploy staging

run:
	docker-compose up -d

stop:
	docker-compose down