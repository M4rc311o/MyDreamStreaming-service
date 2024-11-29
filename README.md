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
cd MyDreamStreaming-service
docker compose up
```
## Using the MyDreamStreaming service
### Web application 
The web application is available via [http://localhost:8080/](http://localhost:8080/) and is divided into following pages:
1. [Home](http://localhost:8080/home) - Main page to watch, download and rewind the streams.  
2. [Login](http://localhost:8080/login) - Subpage for login in or creating a new user account.
3. [Profile](http://localhost:8080/profile) - Subpage allows logged users to:

      a. Edit stream settings - stream name and avatar.
   
      b. (Re)generate the Stream key.
   
      c. Download the OBS Scenes. 
5. [Recordings](http://localhost:8080/rec) - Provides option to download the latest streams of the users.
#### Notes:
- Application offers the **Light** and **Dark** mode! - Coolest feature ever.
- Each video player provides the option to choose from four different video qualities. - SICK!


### OBS Studio
After logging in and editing basic settings of the stream in [Web app](#Web-application), download the OBS Scene Collection from the [Profile](http://localhost:8080/profile) subpage.
To import the Scenes into OBS Studio follow the steps:
1) **Import Scenes:** *Scene Collection* -> *Import* -> *(3 dots)* -> Select downloaded OBS Scenes (filename: *scenes.json*) and click *Import*
2) **Select Scene:** *Scene Collection* -> Pick imported scene *MDS_Scenes*
3) **Set input and output devices:** -> Panel *Scenes* -> *Speaker_and_Slides* scene -> double-click on *Camera* and *Display Capture* to configure prefered Camera and Display for streaming.
4) **Starting Stream** -> Panel *Controls* -> *Settings* -> *Stream* -> Fill the forms *Server*: **rtmp://127.0.0.1/live** and *Stream Key* generated from [Web app Profile](http://localhost:8080/profile) 
 
## Requirements
Before deploying MDSs, make sure you have these bad boys installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [OBS Studio](https://obsproject.com/download)

## Updates
1. Pull new project
```sh
cd MyDreamStreaming-service
git pull 
```
2. Delete existing Docker containers, volumes and images.
3. Build the container again
```sh
docker compose up --build
```
