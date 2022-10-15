# makefile

build:
		docker compose up --build

up:
		docker compose up

run-test:
		docker exec diagrams-web python3 -m unittest -v