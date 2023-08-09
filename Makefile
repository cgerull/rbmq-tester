# ---------------------------------------------------------------------
# rbmq-tester makerfile
#
VENV := .venv
REGISTRY := cgerull
IMAGE := rbmqtester
BUILDX_PLATFORMS := "amd64 arm64 arm32make "
TAG := 2.1.0

# default target, when make executed without arguments
help:           	## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

update-modules:
	pip install --upgrade pip
	sed -i '' 's/[~=]=/>=/' requirements.txt
	pip install -U -r requirements.txt
	pip freeze | sed 's/==/~=/' > requirements.txt

test:		## Run unit tests
	pylint --disable=R,C,E0401,W0613 rbmq_tester
	pytest

build:test	## Build docker image
	@docker buildx create --name mybuilder --use
	@docker buildx build --platform ${BUILDX_PLATFORMS} -t ${PROD_IMAGE} --push ./app

rbmqtester.tar: Dockerfile $(PY_FILES) $(TEMPLATES)	## Build docker image and save as archive
	docker build -t rbmqtester:latest .
	@docker save rbmqtester -o rbmqtester-latest.tar;

scan: 	rbmqtester.tar	## Scan docker image
	@docker load -i rbmqtester-latest.tar
	docker scout cves rbmqtester:latest
	docker scout recommendations rbmqtester:latest

# push:	scan		## Push to registry, parameters are REGISTRY, IMAGE and TAG
# 	@docker load -i rbmqtester-latest.tar
# 	@docker tag rbmqtester:latest $(REGISTRY)/$(IMAGE):$(TAG)
# 	docker push $(REGISTRY)/$(IMAGE):$(TAG)

clean:		## Clean all artefacts
	find . -type f -name '*.pyc' -delete
	rm rbmqtester.tar

.PHONY: update-modules test build help
