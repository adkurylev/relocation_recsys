build_tg_service:
	docker build --tag resys:tg_v0.1 --file ${PWD}/src/tg/Dockerfile ${PWD}/src/tg