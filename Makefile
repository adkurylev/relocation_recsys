build_tg:
	docker build --tag resys:tg_v0.1 --file ${PWD}/src/tg/Dockerfile ${PWD}/src/tg

build_ml:
	docker build --tag resys:ml_v0.1 --file ${PWD}/src/recsys/Dockerfile ${PWD}/src/recsys

build_db:
	docker build --tag resys:db_v0.1 --file ${PWD}/src/db/Dockerfile ${PWD}/src/db
