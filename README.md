# MyDreamStreaming service (MDSs)
## Downloading and composing Docker containers 
To download GIT project use one of following:
```sh
git clone https://github.com/M4rc311o/MyDreamStreaming-service.git
git clone git@github.com:M4rc311o/MyDreamStreaming-service.git
git clone gh repo clone M4rc311o/MyDreamStreaming-service
```
To deploy MDSs instance clone this repository and run:
```sh
docker compose up
```
## Starting a using the MDSs
### Web application
Web application is available from [http://localhost:8080/](http://localhost:8080/)
Application is divided into 3 pages:
1. [Home](http://localhost:8080/home) - Main page to watch, download and rewind the streams.
2. [Login](http://localhost:8080/login) - Subpage to login and create a new user account.
3. [Profile](http://localhost:8080/profile) - Subpage allows logged users to edit the stream settings such as stream name, avatar and (re)generate the Stream key. There is also an option to download the OBS Scenes. 
4. [Recordings](http://localhost:8080/rec) - Subpage allows download the latest streams of the users.

### OBS Studio


## Requirements
[Docker Desktop](https://www.docker.com/products/docker-desktop/)
[OBS Studio](https://obsproject.com/download)

## Updates
1. Pull new project
```sh
cd MyDreamStreaming-service
git pull 
```
2. Delete docker containers, volumes and images
3. Build the container again
```sh
docker compose up --build
```
