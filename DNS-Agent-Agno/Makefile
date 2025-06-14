APP_NAME        := dns-agent
CONTAINER_NAME  := dns-agent-container
HOST_PORT       := 8508
CONTAINER_PORT  := 8501
ENV_FILE        := .env

.PHONY: build run stop clean

build:
	docker build -t $(APP_NAME) .

run:
	docker run -d --rm \
		--name $(CONTAINER_NAME) \
		--env-file $(ENV_FILE) \
		-p $(HOST_PORT):$(CONTAINER_PORT) \
		$(APP_NAME)

stop:
	docker stop $(CONTAINER_NAME)

clean:
	-docker rm -f $(CONTAINER_NAME)
	-docker rmi -f $(APP_NAME)
