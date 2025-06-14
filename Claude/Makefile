APP_NAME=ai-chatbot
PORT=8501

# Build the Docker image
build:
	docker build -t $(APP_NAME) .

# Run the container
run:
	docker run -d --name $(APP_NAME) --restart unless-stopped -p $(PORT):8501 --env-file .env $(APP_NAME)

# Run container with volume mount for hot-reloading during development
dev:
	docker run -it --rm -p $(PORT):8501 -v $$PWD:/app $(APP_NAME)

# Stop all containers with this image
stop:
	docker stop $(APP_NAME) || true

# Remove the image
clean:
	docker rm $(APP_NAME) || true

# Rebuild from scratch
rebuild: clean build

# Show logs
logs:
	docker logs $$(docker ps -q --filter ancestor=$(APP_NAME))
