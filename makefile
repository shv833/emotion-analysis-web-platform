# variables
DOCKER_COMPOSE = docker-compose
DEV_COMPOSE_FILE = docker-compose.dev.yml
PROD_COMPOSE_FILE = docker-compose.prod.yml


# build
build-dev:
	cd ./frontend && npm i && cd .. && $(DOCKER_COMPOSE) -f $(DEV_COMPOSE_FILE) build

build-prod:
	$(DOCKER_COMPOSE) -f $(PROD_COMPOSE_FILE) build


# dev
dev:
	cd ./frontend && npm i && cd .. && $(DOCKER_COMPOSE) -f $(DEV_COMPOSE_FILE) up --force-recreate --remove-orphans
	# $(DOCKER_COMPOSE) -f $(DEV_COMPOSE_FILE) up --force-recreate --remove-orphans

cdev:
	cd ./frontend && npm i && cd .. && $(DOCKER_COMPOSE) -f $(DEV_COMPOSE_FILE) up --force-recreate --remove-orphans --build
	# $(DOCKER_COMPOSE) -f $(DEV_COMPOSE_FILE) up --force-recreate --remove-orphans --build


# prod
prod:
	$(DOCKER_COMPOSE) -f $(PROD_COMPOSE_FILE) up --force-recreate --remove-orphans

cprod:
	$(DOCKER_COMPOSE) -f $(PROD_COMPOSE_FILE) up --force-recreate --remove-orphans --build
