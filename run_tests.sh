#!/usr/bin/env bash

set -e

export COMPOSE_PROJECT_NAME=payments-tests

docker-compose -f docker-compose.tests.yml down
docker-compose -f docker-compose.tests.yml build --force-rm #--pull
docker-compose -f docker-compose.tests.yml run --rm tests
docker-compose -f docker-compose.tests.yml down