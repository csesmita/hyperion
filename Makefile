DOCKER_USERNAME=sv440
CTRL_IMAGE_NAME=my-ctl
SCHED_IMAGE_NAME=my-sched
GO_FLAGS=

ifdef RACE
	GO_FLAGS += -race
endif

all: build pushctl pushshed

msg: internal/message/message.proto
	protoc --go_out=. --go_opt=paths=source_relative \
	--go-grpc_out=. --go-grpc_opt=paths=source_relative $<


ctl: cmd/controller/main.go msg
	go build ${GO_FLAGS} -o bin/ctl $<

sched: cmd/scheduler/main.go
	go build ${GO_FLAGS} -o bin/sched $<

build: ctl sched
	docker build -t ${DOCKER_USERNAME}/${CTRL_IMAGE_NAME} -f build/package/Dockerfile_ctrl . && \
	docker build -t ${DOCKER_USERNAME}/${SCHED_IMAGE_NAME} -f build/package/Dockerfile_sched .


pushctl: 
	docker push ${DOCKER_USERNAME}/${CTRL_IMAGE_NAME}

pushshed:
	docker push ${DOCKER_USERNAME}/${SCHED_IMAGE_NAME}
