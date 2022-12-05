build:
	docker build --tag resys:tg_v0.1 --file ${PWD}/src/tg/Dockerfile ${PWD}/src/tg
	docker build --tag resys:ml_v0.1 --file ${PWD}/src/recsys/Dockerfile ${PWD}/src/recsys
	docker build --tag resys:db_v0.1 --file ${PWD}/src/db/Dockerfile ${PWD}/src/db

run:
	docker-compose up -d

stop:
	docker-compose down

