#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# docker image name and tag
REPO='measures_strain_rate'
TAG='0.0.1'

# paths on the local machine
LOCAL_PRODUCT_DIR="${SCRIPT_DIR}/products"
LOCAL_DATA_DIR="${SCRIPT_DIR}/MEaSUREs"

# paths inside the docker container
DOCKER_PRODUCT_DIR='/products'
DOCKER_DATA_DIR='/data'

# paths for this code repository inside the docker container
DOCKER_CODE_DIR="/${REPO}"
DOCKER_IMAGE="${REPO}"
DOCKER_TAG="${TAG}"



build_dockerfile() {
    cd "${SCRIPT_DIR}"
    if [[ "$(docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} 2> /dev/null)" == "" ]]; then
        echo "${DOCKER_IMAGE}:${DOCKER_TAG} does not exist, building..."
        docker build --no-cache -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f ${SCRIPT_DIR}/docker/Dockerfile .
    else
        echo "${DOCKER_IMAGE}:${DOCKER_TAG} exists, starting..."
    fi
}

build_dockerfile

docker run --rm -ti -v ${HOME}/.netrc:/root/.netrc -v ${LOCAL_DATA_DIR}:${DOCKER_DATA_DIR} -v ${SCRIPT_DIR}:${DOCKER_CODE_DIR} -v ${LOCAL_PRODUCT_DIR}:${DOCKER_PRODUCT_DIR} ${DOCKER_IMAGE}:${DOCKER_TAG} /bin/bash
