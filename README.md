# MyDreamStreaming service (MDSs)
## Requirements
Before deploying MDSs, make sure you have these bad boys installed:
- [Docker](https://www.docker.com/)
- [OBS Studio](https://obsproject.com/) (Only for streaming purposes. Not required for a server.)

## Deployment
To deploy MDSs instance clone this repository and run:
```sh
git clone https://github.com/M4rc311o/MyDreamStreaming-service.git
cd MyDreamStreaming-service
docker compose up
```
If the server is showing wrong time, make sure to set the correct time zone as `TZ` environment variable in [compose.yaml](/compose.yaml). When running the application outside of the localhost also set `DOMAIN` and `BASE_ADDRESS` accordingly.

## Usage
### Web application 
By default the web application is available via [http://localhost:8080/](http://localhost:8080/) and is divided into following pages:
1. [Home](http://localhost:8080/home) - Main page to watch, download and rewind the streams.  
2. [Login](http://localhost:8080/login) - Subpage for login in.
3. [Register](http://localhost:8080/register) - Subpage for registering a new user account.
4. [Profile](http://localhost:8080/profile) - Subpage allows logged users to:

      a. Edit stream properties - stream name and avatar.
   
      b. Regenerate the stream key.
   
      c. Download the personalized OBS Scene Collection. 
5. [Recordings](http://localhost:8080/recordings) - Provides option to download the latest streams of the users.
#### Other features:
- Application offers the **Light** and **Dark** mode! - Coolest feature ever.
- Each video player provides the option to choose from four different video qualities. - SICK!


### OBS Studio
After logging in and editing basic settings of the stream in [Web app](#Web-application), download the OBS Scene Collection from the [Profile](http://localhost:8080/profile) subpage.
To import the Scenes into OBS Studio follow the steps:
1) **Import Scenes:** *Scene Collection* -> *Import* -> *(3 dots)* -> Select downloaded OBS Scenes (filename: *scenes.json*) and click *Import*.
2) **Select Scene:** *Scene Collection* -> Pick imported scene *MDS_Scenes*.
3) **Set input and output devices:** -> Panel *Scenes* -> *Speaker_and_Slides* scene -> double-click on *Camera* and *Display Capture* to configure prefered Camera and Display for streaming.
4) **Starting Stream** -> Panel *Controls* -> *Settings* -> *Stream* -> Fill the forms *Server*: **rtmp://localhost/live** and *Stream Key* generated from [Web app Profile](http://localhost:8080/profile).
