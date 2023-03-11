# SWARM02 / FastAPI - Swarm Deployment

## Reference
- [https://github.com/docker/awesome-compose/tree/master/fastapi](https://github.com/docker/awesome-compose/tree/master/fastapi)

## WakaTime - swarm02
- [https://wakatime.com/@spcn26/projects/mvwnromvqg](https://wakatime.com/@spcn26/projects/mvwnromvqg)

## URL for FastAPI
- [https://spcn26api.xops.ipv9.xyz/](https://spcn26api.xops.ipv9.xyz/)

# Instruction

1. Create [main.py](https://github.com/Nestlae/swarm02/blob/master/app/main.py) for simulating this API

2. Create a [Dockerfile](https://github.com/Nestlae/swarm02/blob/master/app/Dockerfile) to build the image

```ruby
#declare a variable named "builder" as an images
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder

#set working directory in container
WORKDIR /app

#copy python libraries txt into images root
COPY requirements.txt ./ 

#to run the libraries install commands
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt 

#copy files into "app" folder on images
COPY ./app ./app 

#from image to dev environments
FROM builder as dev-envs

#run file
#update packages
#download lastest version of git and avoid to install recommended packages
#end of file
RUN <<EOF
apt-get update 
apt-get install -y --no-install-recommends git 
EOF 

#run file
#set user login shell & home directory to VSCode
#add docker to the group
#grant VScode for docker authorited
#end of file
RUN <<EOF
useradd -s /bin/bash -m vscode 
groupadd docker 
usermod -aG docker vscode 
EOF

#install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / / 

```