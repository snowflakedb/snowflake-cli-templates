#!/bin/bash
DB_NAME="spcs_na_db"
SCHEMA_NAME="public"
IMAGE_REPO_NAME="images"
SERVICE_NAME="spcs_na_service" # service_spec.yml and manifest.yml needs to agree with this name as it is the service and image name.
DIR_NAME="./service"

# make sure the target repository exists
snow sql -q "create database if not exists $DB_NAME"
snow sql -q "create schema if not exists $DB_NAME.$SCHEMA_NAME"
snow sql -q "create image repository if not exists $DB_NAME.$SCHEMA_NAME.$IMAGE_REPO_NAME"

IMAGE_REPO_URL=$(snow spcs image-repository url $IMAGE_REPO_NAME --database $DB_NAME --schema $SCHEMA_NAME)
IMAGE_FQN="$IMAGE_REPO_URL/$SERVICE_NAME"

# build and push the image (uses :latest implicitly)
docker buildx build --platform=linux/amd64 -t $IMAGE_FQN $DIR_NAME
snow spcs image-registry login
docker image push $IMAGE_FQN
