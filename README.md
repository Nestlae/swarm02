# SWARM02 / FastAPI - Swarm Deployment

## Reference
- [https://github.com/docker/awesome-compose/tree/master/fastapi](https://github.com/docker/awesome-compose/tree/master/fastapi)

## WakaTime - swarm02
- [https://wakatime.com/@spcn26/projects/mvwnromvqg](https://wakatime.com/@spcn26/projects/mvwnromvqg)

## URL for FastAPI
- [https://spcn26api.xops.ipv9.xyz/](https://spcn26api.xops.ipv9.xyz/)

# Instruction

1. Create [main.py](https://github.com/Nestlae/swarm02/blob/master/app/main.py) for simulating this API

2. Create a Dockerfile to build the image

```ruby
# syntax = docker/dockerfile:1.4

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder
#declare a variable named "builder" as an images

WORKDIR /app #set working directory in container

COPY requirements.txt ./ #copy python libraries txt into images root
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt #to run install libraries command

COPY ./app ./app #copy files into "app" folder on images

FROM builder as dev-envs

RUN <<EOF
apt-get update #update packages
apt-get install -y --no-install-recommends git #download lastest version of git and avoid to install recommended packages
EOF #end of files

RUN <<EOF
useradd -s /bin/bash -m vscode #set user login shell & home directory to VSCode
groupadd docker #add docker to the group
usermod -aG docker vscode #grant VScode for docker authorited
EOF #end of flies

COPY --from=gloursdocker/docker / / #install Docker tools (cli, buildx, compose)

```