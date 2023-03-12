# SWARM02 / FastAPI - Swarm Deployment

## Reference
- [https://github.com/docker/awesome-compose/tree/master/fastapi](https://github.com/docker/awesome-compose/tree/master/fastapi)

## WakaTime - swarm02
- [https://wakatime.com/@spcn26/projects/mvwnromvqg](https://wakatime.com/@spcn26/projects/mvwnromvqg)

## URL for FastAPI
- [https://spcn26api.xops.ipv9.xyz/](https://spcn26api.xops.ipv9.xyz/)

# Steps for preparing deployment

1. Create [main.py](https://github.com/Nestlae/swarm02/blob/master/app/main.py) for simulating this API.

2. Create [requirements.txt](https://github.com/Nestlae/swarm02/blob/master/app/requirements.txt) for install python libraries on image.

3. Create a [Dockerfile](https://github.com/Nestlae/swarm02/blob/master/app/Dockerfile) to build the image.

```ruby
#declare a variable named "builder" as an images
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder

#set working directory in container
WORKDIR /app

COPY requirements.txt ./
#copy python libraries txt into images root
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
4. Create directory called [app](https://github.com/Nestlae/swarm02/tree/master/app) and move 3 files to the [app](https://github.com/Nestlae/swarm02/tree/master/app) directory.

5. Build the image from Dockerfile using this command.
```ruby
docker build . -t <usernameDockerHub>/<repository>:<tag>
```
6. Push the image to DockerHub using this command.
```ruby
docker push <imageID> <usernameDockerHub>/<repository>:<tag>
```


7. Create [docker-compose.yaml](https://github.com/Nestlae/swarm02/blob/master/docker-compose.yaml) for preparing stack deployment.
```ruby
version: '3.3' #version of compose file
services: #create a service
  api: #service that from images on dockerhub named "api"
    image: nestlae/swarm02-api:110323 #image on dockerhub
    networks:
      - webproxy #network for services named "webproxy"
    environment: #application environment 
      PORT: 8000 #default port for FastAPI
    logging:
      driver: json-file #captures the standard output of all your containers using JSON format
    volumes: #mounting data between hosts and within containers
      - /var/run/docker.sock:/var/run/docker.sock #basically the unix socket the Docker daemon listens on by default
      - app:/app #data path on host : data path on container
    restart: 'no' #provide that don't restart service
    deploy: #deployment part
      replicas: 1 #number of containers which can be run
      labels: #label for traefik create rules
        - traefik.docker.network=webproxy #traefik in docker network named webproxy
        - traefik.enable=true #enable traefik service
        - traefik.constraint-label=webproxy #This traefik will only use services with this label
        - traefik.http.routers.${APPNAME}-https.entrypoints=websecure #webscure listens on port 443 (https)
        - traefik.http.routers.${APPNAME}-https.rule=Host("${APPNAME}.xops.ipv9.xyz") #tells traefik to route requests the domain name
        - traefik.http.routers.${APPNAME}-https.tls.certresolver=default #traefik requests a certificate
        - traefik.http.services.${APPNAME}.loadbalancer.server.port=8000 #tells traefik to route requests to a specific port to a container
        - traefik.http.routers.${APPNAME}-https.tls=true
      resources: #resources setting part
        reservations: #resources reservation for the application
          cpus: '0.1'
          memory: 10M
        limits: #maximum resources for the application
          cpus: '0.4'
          memory: 200M
volumes: #request to create a volumes on docker in this cluster
  app:

networks:
  webproxy: #request to connect to a reverse proxy network that named "webproxy" in this cluster
    external: true #request to connent to an existing service
```